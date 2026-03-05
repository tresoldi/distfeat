"""Dataset model and loaders for distfeat."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

import distfeat.resources as resources

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path


@dataclass(frozen=True)
class FeatureDataset:
    """Container for the canonical feature TSV data."""

    sounds: Mapping[str, str]
    classes: Mapping[str, tuple[str, str, tuple[str, ...]]]
    features: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        immutable_sounds = MappingProxyType(dict(self.sounds))
        immutable_classes = MappingProxyType(
            {
                name: (desc, feat_str, tuple(graphemes))
                for name, (desc, feat_str, graphemes) in self.classes.items()
            },
        )
        immutable_features = tuple((value, feature) for value, feature in self.features)

        object.__setattr__(self, "sounds", immutable_sounds)
        object.__setattr__(self, "classes", immutable_classes)
        object.__setattr__(self, "features", immutable_features)

    def __getstate__(
        self,
    ) -> tuple[
        dict[str, str],
        dict[str, tuple[str, str, tuple[str, ...]]],
        tuple[tuple[str, str], ...],
    ]:
        """Serialize with pickle-friendly containers."""
        return dict(self.sounds), dict(self.classes), tuple(self.features)

    def __setstate__(
        self,
        state: tuple[
            dict[str, str],
            dict[str, tuple[str, str, tuple[str, ...]]],
            tuple[tuple[str, str], ...],
        ],
    ) -> None:
        """Restore immutable containers after unpickling."""
        sounds, classes, features = state
        object.__setattr__(self, "sounds", MappingProxyType(dict(sounds)))
        object.__setattr__(
            self,
            "classes",
            MappingProxyType(
                {
                    name: (desc, feat_str, tuple(graphemes))
                    for name, (desc, feat_str, graphemes) in classes.items()
                },
            ),
        )
        object.__setattr__(self, "features", tuple(features))

    @property
    def feature_values(self) -> dict[str, set[str]]:
        """Return FEATURE -> set[VALUE]."""
        result: dict[str, set[str]] = {}
        for value, feature in self.features:
            result.setdefault(feature, set()).add(value)
        return result

    @property
    def class_graphemes(self) -> dict[str, frozenset[str]]:
        """Return SOUND_CLASS -> frozenset[GRAPHEME]."""
        return {name: frozenset(data[2]) for name, data in self.classes.items()}

    @property
    def class_features(self) -> dict[str, str]:
        """Return SOUND_CLASS -> FEATURES string."""
        return {name: data[1] for name, data in self.classes.items()}


def load_builtin_dataset() -> FeatureDataset:
    """Load the bundled TSV dataset."""
    return resources.load_builtin_dataset()


def load_dataset(
    directory: str | Path | None = None,
    *,
    sounds_path: str | Path | None = None,
    classes_path: str | Path | None = None,
    features_path: str | Path | None = None,
) -> FeatureDataset:
    """Load a dataset from a directory or explicit file paths."""
    return resources.load_dataset(
        directory=directory,
        sounds_path=sounds_path,
        classes_path=classes_path,
        features_path=features_path,
    )


def dataset_from_rows(
    *,
    sounds: Mapping[str, str],
    classes: Mapping[str, tuple[str, str, Sequence[str]]],
    features: Sequence[tuple[str, str]],
) -> FeatureDataset:
    """Build a dataset directly from in-memory rows."""
    return FeatureDataset(
        sounds=sounds,
        classes={
            name: (desc, feat_str, tuple(graphemes))
            for name, (desc, feat_str, graphemes) in classes.items()
        },
        features=tuple(features),
    )
