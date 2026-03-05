"""Default IPA categorical feature system."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

from distfeat.systems.categorical import (
    FEATURE_CATEGORIES,
    CategoricalFeatureSystem,
    normalize_input_grapheme,
)

if TYPE_CHECKING:
    from distfeat.dataset import FeatureDataset

_TONE_VALUES = frozenset(
    {
        "with_downstep",
        "with_extra-high_tone",
        "with_extra-low_tone",
        "with_falling_tone",
        "with_global_fall",
        "with_global_rise",
        "with_high_tone",
        "with_low_tone",
        "with_mid_tone",
        "with_rising_tone",
        "with_upstep",
    }
)


def _parse_name_to_features(name: str) -> frozenset[str]:
    """Parse a sound NAME string from sounds.tsv into a feature set."""
    features: set[str] = set()
    for word in name.split():
        value = word.lower().strip()
        if value in _TONE_VALUES:
            features.add(value)
            continue
        value = value.replace("_", "-")
        if value in FEATURE_CATEGORIES:
            features.add(value)
    return frozenset(features)


@dataclass(frozen=True)
class IPAFeatureSystem(CategoricalFeatureSystem):
    """Built-in IPA categorical feature system."""

    dataset: FeatureDataset

    @property
    def name(self) -> str:
        return "ipa"

    @cached_property
    def _grapheme_table(self) -> dict[str, frozenset[str]]:
        table: dict[str, frozenset[str]] = {}
        for grapheme, name in self.dataset.sounds.items():
            features = _parse_name_to_features(name)
            if features:
                table[normalize_input_grapheme(grapheme)] = features
        return table
