"""Tresoldi feature system."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

from distfeat.systems.categorical import (
    CategoricalFeatureSystem,
    normalize_input_grapheme,
)

if TYPE_CHECKING:
    from distfeat.dataset import FeatureDataset


@dataclass(frozen=True)
class TresoldiFeatureSystem(CategoricalFeatureSystem):
    """Built-in Tresoldi feature system."""

    dataset: FeatureDataset

    @property
    def name(self) -> str:
        return "tresoldi"

    @cached_property
    def _grapheme_table(self) -> dict[str, frozenset[str]]:
        table: dict[str, frozenset[str]] = {}
        for grapheme, name in self.dataset.sounds.items():
            features: set[str] = set()
            for word in name.split():
                value = word.lower().strip()
                if value:
                    if not value.startswith("with_"):
                        value = value.replace("_", "-")
                    features.add(value)
            if features:
                table[normalize_input_grapheme(grapheme)] = frozenset(
                    features,
                )
        return table
