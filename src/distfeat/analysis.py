"""Higher-level analysis helpers built on top of feature systems."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import TYPE_CHECKING

from distfeat.registry import get_registry, get_system

if TYPE_CHECKING:
    from distfeat.protocol import FeatureSystem


@dataclass(frozen=True)
class FeatureMatrix:
    """A compact tabular view of distinguishing feature information."""

    columns: tuple[str, ...]
    rows: dict[str, tuple[object, ...]]
    system: str
    mode: str


def _lookup_features(grapheme: str, system_obj: FeatureSystem) -> frozenset[str]:
    """Resolve a grapheme or class symbol to a feature set."""
    class_features = system_obj.class_features(grapheme)
    if class_features is not None:
        return class_features

    features = system_obj.grapheme_to_features(grapheme)
    if features is None:
        msg = f"Unknown grapheme or sound class: {grapheme!r}"
        raise KeyError(msg)
    return features


def _signature_is_unique(
    rows: dict[str, dict[str, object]],
    columns: tuple[str, ...],
) -> bool:
    """Check whether the selected columns uniquely identify all rows."""
    seen: set[tuple[object, ...]] = set()
    for row_name in sorted(rows):
        signature = tuple(rows[row_name].get(column, 0.0) for column in columns)
        if signature in seen:
            return False
        seen.add(signature)
    return True


def _select_minimal_columns(rows: dict[str, dict[str, object]]) -> tuple[str, ...]:
    """Return the smallest column subset that distinguishes all rows."""
    if not rows:
        return ()

    candidates = tuple(sorted({column for data in rows.values() for column in data}))
    if len(rows) <= 1:
        return ()

    for size in range(1, len(candidates) + 1):
        for subset in combinations(candidates, size):
            if _signature_is_unique(rows, subset):
                return subset

    return candidates


def features_to_graphemes(
    query: frozenset[str],
    *,
    system: str | None = None,
    exact: bool = False,
) -> list[str]:
    """Return all graphemes that satisfy the requested feature query."""
    registry = get_registry()
    system_obj = registry.get_system(system)
    matches: list[str] = []

    for grapheme in sorted(registry.dataset.sounds):
        features = system_obj.grapheme_to_features(grapheme)
        if features is None:
            continue

        matched = features == query if exact else system_obj.partial_match(query, features)
        if matched:
            matches.append(grapheme)

    return matches


def derive_class_features(
    graphemes: list[str] | tuple[str, ...],
    *,
    system: str | None = None,
) -> frozenset[str]:
    """Derive the strict shared feature intersection of a grapheme set."""
    if not graphemes:
        msg = "Cannot derive class features from an empty grapheme set."
        raise ValueError(msg)

    system_obj = get_system(system)
    feature_sets = [_lookup_features(grapheme, system_obj) for grapheme in graphemes]

    common = set(feature_sets[0])
    for feature_set in feature_sets[1:]:
        common &= feature_set

    return frozenset(common)


def minimal_matrix(
    graphemes: list[str] | tuple[str, ...],
    *,
    system: str | None = None,
) -> FeatureMatrix:
    """Return a minimal distinguishing feature matrix for the given graphemes."""
    if not graphemes:
        msg = "Cannot build a feature matrix from an empty grapheme set."
        raise ValueError(msg)

    system_obj = get_system(system)
    system_name = system_obj.name

    if system_name == "distinctive" and hasattr(system_obj, "grapheme_to_scalars"):
        scalar_rows: dict[str, dict[str, object]] = {}
        for grapheme in graphemes:
            scalars = system_obj.grapheme_to_scalars(grapheme)  # type: ignore[attr-defined]
            if scalars is None:
                msg = f"Unsupported grapheme for scalar matrix: {grapheme!r}"
                raise KeyError(msg)
            scalar_rows[grapheme] = {name: value for name, value in scalars.items() if value != 0.0}

        columns = _select_minimal_columns(scalar_rows)
        rows = {
            grapheme: tuple(scalar_rows[grapheme].get(column, 0.0) for column in columns)
            for grapheme in graphemes
        }
        return FeatureMatrix(columns=columns, rows=rows, system=system_name, mode="scalar")

    categorical_rows: dict[str, dict[str, object]] = {}
    for grapheme in graphemes:
        features = _lookup_features(grapheme, system_obj)
        categorical_rows[grapheme] = {feature: True for feature in features}

    columns = _select_minimal_columns(categorical_rows)
    rows = {
        grapheme: tuple(bool(categorical_rows[grapheme].get(column, False)) for column in columns)
        for grapheme in graphemes
    }
    return FeatureMatrix(columns=columns, rows=rows, system=system_name, mode="categorical")


def _format_cell(value: object) -> str:
    """Format a matrix cell for display."""
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, float):
        if value.is_integer():
            return f"{value:.1f}"
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


def tabulate_matrix(
    matrix: FeatureMatrix,
    *,
    format: str = "plain",
) -> str:
    """Render a feature matrix as plain text or markdown."""
    if format not in {"plain", "markdown"}:
        msg = f"Unsupported matrix format: {format!r}"
        raise NotImplementedError(msg)

    header = ["grapheme", *matrix.columns]
    body = [
        [grapheme, *[_format_cell(value) for value in matrix.rows[grapheme]]]
        for grapheme in matrix.rows
    ]
    widths = [
        max(len(str(cell)) for cell in [header[index], *[row[index] for row in body]])
        for index in range(len(header))
    ]

    def _render_row(row: list[str]) -> str:
        return " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row))

    if format == "markdown":
        divider = " | ".join("-" * width for width in widths)
        lines = [_render_row(header), divider]
        lines.extend(_render_row(row) for row in body)
        return "\n".join(lines)

    lines = [_render_row(header), "-+-".join("-" * width for width in widths)]
    lines.extend(_render_row(row) for row in body)
    return "\n".join(lines)


def distance(
    grapheme_a: str,
    grapheme_b: str,
    *,
    system: str | None = None,
    precomputed: dict[str, dict[str, float]] | None = None,
) -> float:
    """Return the distance between two graphemes."""
    if precomputed is not None:
        direct = precomputed.get(grapheme_a, {}).get(grapheme_b)
        if direct is not None:
            return direct
        reverse = precomputed.get(grapheme_b, {}).get(grapheme_a)
        if reverse is not None:
            return reverse
        msg = f"Missing precomputed distance for pair: ({grapheme_a!r}, {grapheme_b!r})"
        raise KeyError(msg)

    system_obj = get_system(system)
    features_a = _lookup_features(grapheme_a, system_obj)
    features_b = _lookup_features(grapheme_b, system_obj)
    return system_obj.sound_distance(features_a, features_b)
