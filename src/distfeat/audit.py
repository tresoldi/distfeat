"""Dataset quality audit utilities."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from distfeat.dataset import FeatureDataset


@dataclass(frozen=True)
class DatasetAuditReport:
    """Structured quality report for a FeatureDataset."""

    sound_count: int
    class_count: int
    feature_pair_count: int
    class_reference_count: int
    class_reference_coverage: float
    unreferenced_sounds: tuple[str, ...]
    unknown_class_graphemes: Mapping[str, tuple[str, ...]]
    duplicate_class_graphemes: Mapping[str, tuple[str, ...]]
    unknown_class_features: Mapping[str, tuple[str, ...]]
    feature_value_conflicts: Mapping[str, tuple[str, ...]]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "unknown_class_graphemes",
            MappingProxyType(dict(self.unknown_class_graphemes)),
        )
        object.__setattr__(
            self,
            "duplicate_class_graphemes",
            MappingProxyType(dict(self.duplicate_class_graphemes)),
        )
        object.__setattr__(
            self,
            "unknown_class_features",
            MappingProxyType(dict(self.unknown_class_features)),
        )
        object.__setattr__(
            self,
            "feature_value_conflicts",
            MappingProxyType(dict(self.feature_value_conflicts)),
        )

    @property
    def has_issues(self) -> bool:
        """Return whether any non-empty issue category was detected."""
        return any(
            (
                self.unknown_class_graphemes,
                self.duplicate_class_graphemes,
                self.unknown_class_features,
                self.feature_value_conflicts,
            ),
        )


def _parse_class_features(feature_string: str) -> tuple[str, ...]:
    return tuple(
        token.strip().lstrip("-")
        for token in feature_string.split(",")
        if token.strip()
    )


def audit_dataset(dataset: FeatureDataset) -> DatasetAuditReport:
    """Audit a dataset for common data-quality problems."""
    known_graphemes = set(dataset.sounds)
    known_values = {value for value, _ in dataset.features}

    unknown_class_graphemes: dict[str, tuple[str, ...]] = {}
    duplicate_class_graphemes: dict[str, tuple[str, ...]] = {}
    unknown_class_features: dict[str, tuple[str, ...]] = {}
    all_class_graphemes: list[str] = []

    for class_name, (_, feature_string, graphemes) in dataset.classes.items():
        all_class_graphemes.extend(graphemes)

        missing = sorted({grapheme for grapheme in graphemes if grapheme not in known_graphemes})
        if missing:
            unknown_class_graphemes[class_name] = tuple(missing)

        seen: set[str] = set()
        duplicates_set: set[str] = set()
        for grapheme in graphemes:
            if grapheme in seen:
                duplicates_set.add(grapheme)
            else:
                seen.add(grapheme)
        duplicates = sorted(duplicates_set)
        if duplicates:
            duplicate_class_graphemes[class_name] = tuple(duplicates)

        class_features = _parse_class_features(feature_string)
        unknown_features = sorted(
            {feature for feature in class_features if feature not in known_values},
        )
        if unknown_features:
            unknown_class_features[class_name] = tuple(unknown_features)

    referenced = set(all_class_graphemes)
    unreferenced_sounds = tuple(sorted(known_graphemes - referenced))
    coverage = (
        (len(referenced & known_graphemes) / len(known_graphemes))
        if known_graphemes
        else 1.0
    )

    value_to_features: dict[str, set[str]] = {}
    for value, feature in dataset.features:
        value_to_features.setdefault(value, set()).add(feature)

    conflicts = {
        value: tuple(sorted(features))
        for value, features in value_to_features.items()
        if len(features) > 1
    }

    return DatasetAuditReport(
        sound_count=len(dataset.sounds),
        class_count=len(dataset.classes),
        feature_pair_count=len(dataset.features),
        class_reference_count=len(all_class_graphemes),
        class_reference_coverage=coverage,
        unreferenced_sounds=unreferenced_sounds,
        unknown_class_graphemes=unknown_class_graphemes,
        duplicate_class_graphemes=duplicate_class_graphemes,
        unknown_class_features=unknown_class_features,
        feature_value_conflicts=conflicts,
    )
