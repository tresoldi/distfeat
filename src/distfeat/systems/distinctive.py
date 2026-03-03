"""Unified distinctive feature system with scalar values."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import distfeat.common as common
from distfeat.dataset import FeatureDataset
from distfeat.geometry import DEFAULT_GEOMETRY, _node_depth
from distfeat.representations import CategoricalFeatures
from distfeat.systems.ipa import (
    FEATURE_CATEGORIES,
    build_class_table,
    normalize_input_grapheme,
    normalize_output_grapheme,
    resolve_alias,
)


@dataclass(frozen=True)
class ScalarDimension:
    """A scalar dimension mapping IPA features to +1.0/-1.0."""

    name: str
    positive: frozenset[str]
    negative: frozenset[str]
    geometry_node: str


_SCALAR_DIMENSIONS: tuple[ScalarDimension, ...] = (
    ScalarDimension("voice", frozenset({"voiced"}), frozenset({"voiceless"}), "Laryngeal"),
    ScalarDimension("spread_glottis", frozenset({"aspirated"}), frozenset(), "Laryngeal"),
    ScalarDimension("constricted_glottis", frozenset({"glottalized"}), frozenset(), "Laryngeal"),
    ScalarDimension(
        "sonorant",
        frozenset({"vowel", "nasal", "approximant", "lateral"}),
        frozenset({"consonant"}),
        "Manner",
    ),
    ScalarDimension(
        "continuant",
        frozenset({"fricative", "approximant"}),
        frozenset({"stop", "affricate"}),
        "Manner",
    ),
    ScalarDimension("nasal", frozenset({"nasal"}), frozenset(), "Manner"),
    ScalarDimension("lateral", frozenset({"lateral"}), frozenset(), "Manner"),
    ScalarDimension("strident", frozenset({"sibilant"}), frozenset(), "Manner"),
    ScalarDimension("delayed_release", frozenset({"affricate"}), frozenset(), "Manner"),
    ScalarDimension("tap_feature", frozenset({"tap"}), frozenset(), "Manner"),
    ScalarDimension(
        "syllabic",
        frozenset({"vowel", "syllabic"}),
        frozenset({"consonant", "non-syllabic"}),
        "Manner",
    ),
    ScalarDimension(
        "labial",
        frozenset({"bilabial", "labio-dental", "labio-velar", "labio-palatal", "labial"}),
        frozenset(),
        "Labial",
    ),
    ScalarDimension("round", frozenset({"rounded"}), frozenset({"unrounded"}), "Labial"),
    ScalarDimension(
        "coronal",
        frozenset(
            {
                "dental",
                "alveolar",
                "post-alveolar",
                "alveolo-palatal",
                "retroflex",
                "linguolabial",
            }
        ),
        frozenset(),
        "Coronal",
    ),
    ScalarDimension(
        "anterior",
        frozenset({"dental", "alveolar"}),
        frozenset({"post-alveolar", "retroflex", "alveolo-palatal"}),
        "Coronal",
    ),
    ScalarDimension(
        "distributed",
        frozenset({"post-alveolar", "alveolo-palatal"}),
        frozenset({"alveolar", "retroflex"}),
        "Coronal",
    ),
    ScalarDimension(
        "dorsal",
        frozenset({"palatal", "palatal-velar", "velar", "uvular"}),
        frozenset(),
        "Dorsal",
    ),
    ScalarDimension("high", frozenset({"close", "near-close"}), frozenset({"open", "near-open"}), "Dorsal"),
    ScalarDimension("low", frozenset({"open", "near-open"}), frozenset({"close", "near-close"}), "Dorsal"),
    ScalarDimension("back", frozenset({"back", "near-back"}), frozenset({"front", "near-front"}), "Dorsal"),
    ScalarDimension("breathy_voice", frozenset({"breathy"}), frozenset(), "Laryngeal"),
    ScalarDimension("creaky_voice", frozenset({"creaky"}), frozenset(), "Laryngeal"),
    ScalarDimension(
        "atr",
        frozenset({"advanced-tongue-root"}),
        frozenset({"retracted-tongue-root"}),
        "TongueRoot",
    ),
    ScalarDimension("apical", frozenset({"apical"}), frozenset({"laminal"}), "Coronal"),
    ScalarDimension("long", frozenset({"long"}), frozenset(), "Prosodic"),
    ScalarDimension("nasalized", frozenset({"nasalized"}), frozenset(), "Prosodic"),
    ScalarDimension("labialized", frozenset({"labialized"}), frozenset(), "Prosodic"),
    ScalarDimension("palatalized", frozenset({"palatalized"}), frozenset(), "Prosodic"),
    ScalarDimension("pharyngealized", frozenset({"pharyngealized"}), frozenset(), "Prosodic"),
    ScalarDimension("ejective", frozenset({"ejective"}), frozenset(), "Prosodic"),
    ScalarDimension("rhotacized", frozenset({"rhotacized"}), frozenset(), "Prosodic"),
    ScalarDimension("velarized", frozenset({"velarized"}), frozenset(), "Prosodic"),
)


def _features_to_scalar(features: frozenset[str]) -> dict[str, float]:
    """Convert categorical features to a scalar representation."""
    result: dict[str, float] = {}
    for dim in _SCALAR_DIMENSIONS:
        if features & dim.positive:
            result[dim.name] = 1.0
        elif dim.negative and features & dim.negative:
            result[dim.name] = -1.0
    return result


def _scalar_to_features(scalars: dict[str, float]) -> frozenset[str]:
    """Convert scalar values back to categorical features."""
    result: set[str] = set()
    dim_map = {dim.name: dim for dim in _SCALAR_DIMENSIONS}
    for name, value in scalars.items():
        dim = dim_map.get(name)
        if dim is None:
            continue
        if value > 0 and dim.positive:
            result.add(next(iter(sorted(dim.positive))))
        elif value < 0 and dim.negative:
            result.add(next(iter(sorted(dim.negative))))
    return frozenset(result)


@dataclass(frozen=True)
class DistinctiveFeatureSystem:
    """Built-in distinctive feature system."""

    dataset: FeatureDataset

    @property
    def name(self) -> str:
        return "distinctive"

    @property
    def representation_kind(self) -> str:
        return "categorical"

    def list_graphemes(self) -> tuple[str, ...]:
        return tuple(sorted(normalize_output_grapheme(grapheme) for grapheme in self._grapheme_table))

    @property
    def dimensions(self) -> tuple[ScalarDimension, ...]:
        return _SCALAR_DIMENSIONS

    @cached_property
    def _dimension_weights(self) -> dict[str, float]:
        weights: dict[str, float] = {}
        for dim in _SCALAR_DIMENSIONS:
            depth = _node_depth(DEFAULT_GEOMETRY, dim.geometry_node, 1) or 2
            weights[dim.name] = 1.0 / depth
        return weights

    @cached_property
    def _grapheme_table(self) -> dict[str, frozenset[str]]:
        table: dict[str, frozenset[str]] = {}
        for grapheme, name in self.dataset.sounds.items():
            features: set[str] = set()
            for word in name.split():
                value = word.lower().strip()
                if not value.startswith("with_"):
                    value = value.replace("_", "-")
                if value in FEATURE_CATEGORIES:
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
            msg = "Distinctive matching requires CategoricalFeatures inputs."
            raise NotImplementedError(msg)
        return self.partial_match(pattern.values, target.values)

    def feature_distance(self, feat_a: str, feat_b: str) -> float:
        return common.feature_distance(feat_a, feat_b)

    def segment_distance(self, a: object, b: object) -> float:
        if not isinstance(a, CategoricalFeatures) or not isinstance(b, CategoricalFeatures):
            msg = "Distinctive segment_distance requires CategoricalFeatures inputs."
            raise NotImplementedError(msg)
        return self.sound_distance(a.values, b.values)

    def grapheme_to_scalars(self, grapheme: str) -> dict[str, float] | None:
        features = self.grapheme_to_features(grapheme)
        if features is None:
            return None
        return _features_to_scalar(features)

    def features_to_scalars(self, features: frozenset[str]) -> dict[str, float]:
        return _features_to_scalar(features)

    def scalars_to_features(self, scalars: dict[str, float]) -> frozenset[str]:
        return _scalar_to_features(scalars)

    def sound_distance(self, feats_a: frozenset[str], feats_b: frozenset[str]) -> float:
        """Geometry-weighted distance using scalar dimensions."""
        if feats_a == feats_b:
            return 0.0

        scalars_a = _features_to_scalar(feats_a)
        scalars_b = _features_to_scalar(feats_b)
        total_weight = 0.0
        total_diff = 0.0

        for dim in _SCALAR_DIMENSIONS:
            weight = self._dimension_weights[dim.name]
            value_a = scalars_a.get(dim.name, 0.0)
            value_b = scalars_b.get(dim.name, 0.0)

            if value_a == 0.0 and value_b == 0.0:
                continue

            total_weight += weight
            total_diff += weight * abs(value_a - value_b) / 2.0

        return total_diff / total_weight if total_weight > 0 else 0.0
