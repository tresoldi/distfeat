"""Dataset model and loaders for distfeat."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import distfeat.resources as resources


@dataclass(frozen=True)
class FeatureDataset:
    """Container for the canonical feature TSV data."""

    sounds: dict[str, str]
    classes: dict[str, tuple[str, str, list[str]]]
    features: list[tuple[str, str]]

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
    classes: Mapping[str, tuple[str, str, list[str]]],
    features: list[tuple[str, str]],
) -> FeatureDataset:
    """Build a dataset directly from in-memory rows."""
    return FeatureDataset(
        sounds=dict(sounds),
        classes={
            name: (desc, feat_str, list(graphemes))
            for name, (desc, feat_str, graphemes) in classes.items()
        },
        features=list(features),
    )
