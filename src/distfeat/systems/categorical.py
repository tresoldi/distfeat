"""Shared base class for categorical feature systems (IPA, Tresoldi, Distinctive)."""

from __future__ import annotations

import unicodedata
from functools import cached_property
from typing import TYPE_CHECKING

import distfeat.common as common
from distfeat.representations import CategoricalFeatures

if TYPE_CHECKING:
    from distfeat.dataset import FeatureDataset


def resolve_alias(feature: str) -> str:
    """Resolve a feature alias to its canonical form."""
    return FEATURE_ALIASES.get(feature, feature)


FEATURE_ALIASES: dict[str, str] = {
    "plosive": "stop",
}

FEATURE_CATEGORIES: dict[str, str] = {
    "plosive": "manner",
    "stop": "manner",
    "fricative": "manner",
    "affricate": "manner",
    "nasal": "manner",
    "approximant": "manner",
    "trill": "manner",
    "tap": "manner",
    "lateral": "manner",
    "click": "manner",
    "implosive": "manner",
    "nasal-click": "manner",
    "bilabial": "place",
    "labio-dental": "place",
    "labio-velar": "place",
    "labio-palatal": "place",
    "dental": "place",
    "alveolar": "place",
    "post-alveolar": "place",
    "alveolo-palatal": "place",
    "retroflex": "place",
    "palatal": "place",
    "palatal-velar": "place",
    "velar": "place",
    "uvular": "place",
    "pharyngeal": "place",
    "epiglottal": "place",
    "glottal": "place",
    "linguolabial": "place",
    "labial": "place",
    "close": "height",
    "near-close": "height",
    "close-mid": "height",
    "mid": "height",
    "open-mid": "height",
    "near-open": "height",
    "open": "height",
    "front": "centrality",
    "near-front": "centrality",
    "central": "centrality",
    "near-back": "centrality",
    "back": "centrality",
    "rounded": "roundedness",
    "unrounded": "roundedness",
    "less-rounded": "rounding",
    "more-rounded": "rounding",
    "voiced": "phonation",
    "voiceless": "phonation",
    "consonant": "type",
    "vowel": "type",
    "long": "duration",
    "mid-long": "duration",
    "ultra-long": "duration",
    "ultra-short": "duration",
    "nasalized": "nasalization",
    "labialized": "labialization",
    "palatalized": "palatalization",
    "labio-palatalized": "palatalization",
    "velarized": "velarization",
    "pharyngealized": "pharyngealization",
    "aspirated": "aspiration",
    "glottalized": "glottalization",
    "breathy": "breathiness",
    "creaky": "creakiness",
    "ejective": "ejection",
    "rhotacized": "rhotacization",
    "syllabic": "syllabicity",
    "non-syllabic": "syllabicity",
    "sibilant": "sibilancy",
    "devoiced": "voicing",
    "revoiced": "voicing",
    "advanced": "relative_articulation",
    "retracted": "relative_articulation",
    "centralized": "relative_articulation",
    "mid-centralized": "relative_articulation",
    "raised": "raising",
    "lowered": "raising",
    "strong": "articulation",
    "unreleased": "release",
    "with-lateral-release": "release",
    "with-nasal-release": "release",
    "with-mid-central-vowel-release": "release",
    "with-frication": "frication",
    "advanced-tongue-root": "tongue_root",
    "retracted-tongue-root": "tongue_root",
    "apical": "laminality",
    "laminal": "laminality",
    "pre-aspirated": "preceding",
    "pre-glottalized": "preceding",
    "pre-labialized": "preceding",
    "pre-nasalized": "preceding",
    "pre-palatalized": "preceding",
    "primary-stress": "stress",
    "secondary-stress": "stress",
}

_IPA_EQUIVALENCES: dict[str, str] = {
    "\u0261": "g",
    "\u2019": "\u02bc",
    "\u0027": "\u02bc",
}

_IPA_REVERSE: dict[str, str] = {
    value: key for key, value in _IPA_EQUIVALENCES.items()
}


def normalize_output_grapheme(grapheme: str) -> str:
    """Map canonical output forms back to preferred IPA graphemes."""
    return "".join(_IPA_REVERSE.get(char, char) for char in grapheme)


def normalize_input_grapheme(grapheme: str) -> str:
    """Normalize lookup graphemes with NFD and IPA equivalences."""
    normalized = unicodedata.normalize("NFD", grapheme)
    return "".join(_IPA_EQUIVALENCES.get(char, char) for char in normalized)


def build_class_table(
    dataset: FeatureDataset,
) -> dict[str, frozenset[str]]:
    """Build SOUND_CLASS -> feature set from the dataset."""
    result: dict[str, frozenset[str]] = {}
    for class_name, feat_str in dataset.class_features.items():
        if feat_str:
            features = frozenset(
                value.strip()
                for value in feat_str.split(",")
                if value.strip()
            )
            if features:
                result[class_name] = features
    return result


class CategoricalFeatureSystem:
    """Shared base for categorical (frozenset-based) feature systems."""

    representation_kind: str = "categorical"

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def _grapheme_table(self) -> dict[str, frozenset[str]]:
        raise NotImplementedError

    def list_graphemes(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                normalize_output_grapheme(g)
                for g in self._grapheme_table
            )
        )

    @cached_property
    def _reverse_table(self) -> dict[frozenset[str], str]:
        result: dict[frozenset[str], str] = {}
        for grapheme, features in self._grapheme_table.items():
            if features not in result:
                result[features] = normalize_output_grapheme(grapheme)
        return result

    @cached_property
    def _class_table(self) -> dict[str, frozenset[str]]:
        return build_class_table(self.dataset)  # type: ignore[attr-defined]

    def grapheme_to_features(
        self, grapheme: str,
    ) -> frozenset[str] | None:
        return self._grapheme_table.get(
            normalize_input_grapheme(grapheme),
        )

    def grapheme_to_representation(
        self, grapheme: str,
    ) -> CategoricalFeatures | None:
        features = self.grapheme_to_features(grapheme)
        if features is None:
            return None
        return CategoricalFeatures(values=features)

    def features_to_grapheme(
        self, features: object,
    ) -> str | None:
        if not isinstance(features, frozenset):
            return None
        return self._reverse_table.get(features)

    def is_class(self, grapheme: str) -> bool:
        return grapheme in self._class_table

    def class_features(
        self, grapheme: str,
    ) -> frozenset[str] | None:
        return self._class_table.get(grapheme)

    def class_representation(
        self, grapheme: str,
    ) -> CategoricalFeatures | None:
        features = self.class_features(grapheme)
        if features is None:
            return None
        return CategoricalFeatures(values=features)

    def add_features(
        self,
        base: frozenset[str],
        added: frozenset[str],
    ) -> frozenset[str]:
        return common.add_features(
            base, added, FEATURE_CATEGORIES, resolve_alias,
        )

    def partial_match(
        self,
        pattern: frozenset[str],
        target: frozenset[str],
    ) -> bool:
        return common.partial_match(pattern, target)

    def matches(self, pattern: object, target: object) -> bool:
        if (
            not isinstance(pattern, CategoricalFeatures)
            or not isinstance(target, CategoricalFeatures)
        ):
            msg = (
                f"{self.name} matching requires"
                " CategoricalFeatures inputs."
            )
            raise NotImplementedError(msg)
        return self.partial_match(pattern.values, target.values)

    def feature_distance(
        self, feat_a: str, feat_b: str,
    ) -> float:
        return common.feature_distance(feat_a, feat_b)

    def segment_distance(self, a: object, b: object) -> float:
        if (
            not isinstance(a, CategoricalFeatures)
            or not isinstance(b, CategoricalFeatures)
        ):
            msg = (
                f"{self.name} segment_distance requires"
                " CategoricalFeatures inputs."
            )
            raise NotImplementedError(msg)
        return self.sound_distance(a.values, b.values)

    def sound_distance(
        self,
        feats_a: frozenset[str],
        feats_b: frozenset[str],
    ) -> float:
        return common.sound_distance(feats_a, feats_b)
