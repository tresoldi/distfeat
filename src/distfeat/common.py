"""Shared helpers for feature-system implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from distfeat.geometry import DEFAULT_GEOMETRY

if TYPE_CHECKING:
    from collections.abc import Callable


def add_features(
    base: frozenset[str],
    added: frozenset[str],
    categories: dict[str, str],
    resolve_fn: Callable[[str], str],
) -> frozenset[str]:
    """Add features and replace others in the same category."""
    result = set(base)
    for feature in added:
        resolved = resolve_fn(feature)
        category = categories.get(resolved)
        if category is not None:
            result = {item for item in result if categories.get(item) != category}
        result.add(resolved)
    return frozenset(result)


def partial_match(pattern: frozenset[str], target: frozenset[str]) -> bool:
    """Check if a pattern matches a target, including negative features."""
    positive = frozenset(value for value in pattern if not value.startswith("-"))
    negative = frozenset(value[1:] for value in pattern if value.startswith("-"))
    return positive <= target and not (negative & target)


def feature_distance(feat_a: str, feat_b: str) -> float:
    """Delegate feature distance to the default geometry."""
    return float(DEFAULT_GEOMETRY.feature_distance(feat_a, feat_b))


def sound_distance(feats_a: frozenset[str], feats_b: frozenset[str]) -> float:
    """Delegate sound distance to the default geometry."""
    return DEFAULT_GEOMETRY.sound_distance(feats_a, feats_b)
