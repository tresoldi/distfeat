"""Native feature representation types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class FeatureState(StrEnum):
    """A symbolic feature value used by multi-state systems."""

    POSITIVE = "+"
    NEGATIVE = "-"
    N = "n"
    DOT = "."
    O = "o"  # noqa: E741
    X = "x"


@dataclass(frozen=True)
class CategoricalFeatures:
    """A set-based categorical feature bundle."""

    values: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class ValuedFeatures:
    """A named feature table with explicit symbolic values."""

    values: dict[str, FeatureState]


type FeatureRepresentation = CategoricalFeatures | ValuedFeatures


def _normalize_valued_query(
    query: dict[str, FeatureState | str],
) -> dict[str, FeatureState]:
    """Normalize a valued query to FeatureState values."""
    return {
        name: value if isinstance(value, FeatureState) else FeatureState(value)
        for name, value in query.items()
    }
