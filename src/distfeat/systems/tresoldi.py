"""Tresoldi feature system."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import distfeat.common as common
from distfeat.dataset import FeatureDataset
from distfeat.representations import CategoricalFeatures
from distfeat.systems.ipa import (
    FEATURE_CATEGORIES,
    build_class_table,
    normalize_input_grapheme,
    normalize_output_grapheme,
    resolve_alias,
)


@dataclass(frozen=True)
class TresoldiFeatureSystem:
    """Built-in Tresoldi feature system."""

    dataset: FeatureDataset

    @property
    def name(self) -> str:
        return "tresoldi"

    @property
    def representation_kind(self) -> str:
        return "categorical"

    def list_graphemes(self) -> tuple[str, ...]:
        return tuple(sorted(normalize_output_grapheme(grapheme) for grapheme in self._grapheme_table))

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
                table[normalize_input_grapheme(grapheme)] = frozenset(features)
        return table

    @cached_property
    def _reverse_table(self) -> dict[frozenset[str], str]:
        result: dict[frozenset[str], str] = {}
        for grapheme, features in self._grapheme_table.items():
            if features not in result:
                result[features] = normalize_output_grapheme(grapheme)
        return result

    @cached_property
    def _class_table(self) -> dict[str, frozenset[str]]:
        return build_class_table(self.dataset)

    def grapheme_to_features(self, grapheme: str) -> frozenset[str] | None:
        return self._grapheme_table.get(normalize_input_grapheme(grapheme))

    def grapheme_to_representation(self, grapheme: str) -> CategoricalFeatures | None:
        features = self.grapheme_to_features(grapheme)
        if features is None:
            return None
        return CategoricalFeatures(values=features)

    def features_to_grapheme(self, features: object) -> str | None:
        if not isinstance(features, frozenset):
            return None
        return self._reverse_table.get(features)

    def is_class(self, grapheme: str) -> bool:
        return grapheme in self._class_table

    def class_features(self, grapheme: str) -> frozenset[str] | None:
        return self._class_table.get(grapheme)

    def class_representation(self, grapheme: str) -> CategoricalFeatures | None:
        features = self.class_features(grapheme)
        if features is None:
            return None
        return CategoricalFeatures(values=features)

    def add_features(self, base: frozenset[str], added: frozenset[str]) -> frozenset[str]:
        return common.add_features(base, added, FEATURE_CATEGORIES, resolve_alias)

    def partial_match(self, pattern: frozenset[str], target: frozenset[str]) -> bool:
        return common.partial_match(pattern, target)

    def matches(self, pattern: object, target: object) -> bool:
        if not isinstance(pattern, CategoricalFeatures) or not isinstance(target, CategoricalFeatures):
            msg = "Tresoldi matching requires CategoricalFeatures inputs."
            raise NotImplementedError(msg)
        return self.partial_match(pattern.values, target.values)

    def feature_distance(self, feat_a: str, feat_b: str) -> float:
        return common.feature_distance(feat_a, feat_b)

    def segment_distance(self, a: object, b: object) -> float:
        if not isinstance(a, CategoricalFeatures) or not isinstance(b, CategoricalFeatures):
            msg = "Tresoldi segment_distance requires CategoricalFeatures inputs."
            raise NotImplementedError(msg)
        return self.sound_distance(a.values, b.values)

    def sound_distance(self, feats_a: frozenset[str], feats_b: frozenset[str]) -> float:
        return common.sound_distance(feats_a, feats_b)
