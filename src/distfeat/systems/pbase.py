"""P-base-derived feature systems with native multi-state support."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import cache, cached_property
from pathlib import Path

from distfeat.representations import FeatureState, ValuedFeatures, _normalize_valued_query

_PBASE_DIR = Path(__file__).resolve().parent.parent / "data" / "pbase"
_FEATURE_FILE = _PBASE_DIR / "ipa2allfeatures.csv"
_SEG_CONVERT_FILE = _PBASE_DIR / "seg_convert.csv"
_SUPPORTED_FAMILIES = ("hc", "jfh", "spe", "uftc")


def _normalize_family(value: str) -> str:
    """Normalize a family name to the internal lowercase form."""
    normalized = value.lower()
    if normalized not in _SUPPORTED_FAMILIES:
        msg = f"Unsupported P-base family: {value!r}"
        raise KeyError(msg)
    return normalized


def _state_from_symbol(value: str) -> FeatureState:
    """Parse a raw symbolic feature value."""
    stripped = value.strip().strip('"')
    return FeatureState(stripped)


def _read_tsv(path: Path) -> list[list[str]]:
    """Read a tab-separated file as rows."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        return list(reader)


@cache
def _pbase_table(family: str) -> dict[str, dict[str, FeatureState]]:
    """Load one bundled P-base feature family with conservative duplicate merging."""
    normalized_family = _normalize_family(family)
    rows = _read_tsv(_FEATURE_FILE)
    header = rows[0]
    body = rows[1:]

    family_columns: list[tuple[int, str]] = []
    for index, raw_name in enumerate(header[1:], start=1):
        name = raw_name.strip().strip('"')
        prefix, suffix = name.split(".", 1)
        if prefix.lower() == normalized_family:
            family_columns.append((index, suffix.strip()))

    result: dict[str, dict[str, FeatureState]] = {}
    for row in body:
        grapheme = row[0]
        values = {
            column_name: _state_from_symbol(row[index])
            for index, column_name in family_columns
        }
        existing = result.get(grapheme)
        if existing is None:
            result[grapheme] = values
            continue
        if existing != values:
            result[grapheme] = {
                key: existing[key] if existing[key] == values[key] else FeatureState.DOT
                for key in existing
            }

    return result


@cache
def _pbase_metadata() -> dict[str, dict[str, str]]:
    """Load optional P-base segment metadata."""
    rows = _read_tsv(_SEG_CONVERT_FILE)
    header = rows[0]
    body = rows[1:]
    result: dict[str, dict[str, str]] = {}
    for row in body:
        entry = {header[index]: row[index] for index in range(len(header))}
        result[entry["ipa"]] = entry
    return result


@dataclass(frozen=True)
class PBaseFeatureSystem:
    """A bundled P-base-derived feature family."""

    family: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "family", _normalize_family(self.family))

    @property
    def name(self) -> str:
        return f"pbase-{self.family}"

    @property
    def representation_kind(self) -> str:
        return "valued"

    def list_graphemes(self) -> tuple[str, ...]:
        return tuple(sorted(self._table))

    @cached_property
    def _table(self) -> dict[str, dict[str, FeatureState]]:
        return _pbase_table(self.family)

    @cached_property
    def _metadata(self) -> dict[str, dict[str, str]]:
        return _pbase_metadata()

    def grapheme_to_representation(self, grapheme: str) -> ValuedFeatures | None:
        values = self._table.get(grapheme)
        if values is None:
            return None
        return ValuedFeatures(values=dict(values))

    def class_representation(self, grapheme: str) -> ValuedFeatures | None:
        return None

    def grapheme_to_features(self, grapheme: str) -> frozenset[str] | None:
        representation = self.grapheme_to_representation(grapheme)
        if representation is None:
            return None
        labels = {f"{name}={state.value}" for name, state in representation.values.items()}
        return frozenset(labels)

    def features_to_grapheme(self, features: object) -> str | None:
        if isinstance(features, ValuedFeatures):
            query = features.values
        elif isinstance(features, dict):
            query = _normalize_valued_query(features)
        else:
            return None

        for grapheme, values in self._table.items():
            if values == query:
                return grapheme
        return None

    def is_class(self, grapheme: str) -> bool:
        return False

    def class_features(self, grapheme: str) -> frozenset[str] | None:
        return None

    def matches(self, pattern: object, target: object) -> bool:
        if isinstance(pattern, ValuedFeatures):
            query = pattern.values
        elif isinstance(pattern, dict):
            query = _normalize_valued_query(pattern)
        else:
            msg = "P-base systems require dict or ValuedFeatures queries."
            raise NotImplementedError(msg)

        if not isinstance(target, ValuedFeatures):
            msg = "P-base matching requires ValuedFeatures targets."
            raise NotImplementedError(msg)

        return all(
            target.values.get(key) == value
            for key, value in query.items()
        )

    def partial_match(self, pattern: frozenset[str], target: frozenset[str]) -> bool:
        msg = "Set-based partial_match is not meaningful for P-base systems."
        raise NotImplementedError(msg)

    def add_features(self, base: frozenset[str], added: frozenset[str]) -> frozenset[str]:
        msg = "Set-based add_features is not meaningful for P-base systems."
        raise NotImplementedError(msg)

    def feature_distance(self, feat_a: str, feat_b: str) -> float:
        return 0.0 if feat_a == feat_b else 1.0

    def segment_distance(self, a: object, b: object) -> float:
        if not isinstance(a, ValuedFeatures) or not isinstance(b, ValuedFeatures):
            msg = "P-base segment_distance requires ValuedFeatures inputs."
            raise NotImplementedError(msg)

        comparable = [
            key
            for key in a.values.keys() | b.values.keys()
            if a.values.get(key, FeatureState.DOT) != FeatureState.DOT
            and b.values.get(key, FeatureState.DOT) != FeatureState.DOT
        ]
        if not comparable:
            return 0.0

        mismatches = sum(1 for key in comparable if a.values.get(key) != b.values.get(key))
        return mismatches / len(comparable)

    def sound_distance(self, feats_a: frozenset[str], feats_b: frozenset[str]) -> float:
        msg = "Set-based sound_distance is not meaningful for P-base systems."
        raise NotImplementedError(msg)
