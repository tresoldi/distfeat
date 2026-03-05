"""Higher-level analysis helpers built on top of feature systems."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import combinations
from typing import TYPE_CHECKING, Literal

from distfeat.registry import get_system
from distfeat.representations import (
    CategoricalFeatures,
    FeatureRepresentation,
    FeatureState,
    ValuedFeatures,
    _normalize_valued_query,
)

if TYPE_CHECKING:
    from distfeat.protocol import FeatureSystem


@dataclass(frozen=True)
class FeatureMatrix:
    """A compact tabular view of distinguishing feature information."""

    columns: tuple[str, ...]
    rows: Mapping[str, tuple[object, ...]]
    system: str
    mode: str


def _lookup_representation(grapheme: str, system_obj: FeatureSystem) -> FeatureRepresentation:
    """Resolve a grapheme or class symbol to its native representation."""
    class_representation = system_obj.class_representation(grapheme)
    if class_representation is not None:
        return class_representation

    representation = system_obj.grapheme_to_representation(grapheme)
    if representation is None:
        msg = f"Unknown grapheme or sound class: {grapheme!r}"
        raise KeyError(msg)
    return representation


def _lookup_categorical(grapheme: str, system_obj: FeatureSystem) -> CategoricalFeatures:
    """Resolve a grapheme or class symbol to a categorical representation."""
    representation = _lookup_representation(grapheme, system_obj)
    if not isinstance(representation, CategoricalFeatures):
        msg = f"System {system_obj.name!r} does not expose categorical features."
        raise NotImplementedError(msg)
    return representation


def _lookup_features(grapheme: str, system_obj: FeatureSystem) -> frozenset[str]:
    """Resolve a grapheme or class symbol to a feature set."""
    return _lookup_categorical(grapheme, system_obj).values


def _lookup_valued(grapheme: str, system_obj: FeatureSystem) -> ValuedFeatures:
    """Resolve a grapheme or class symbol to a valued representation."""
    representation = _lookup_representation(grapheme, system_obj)
    if not isinstance(representation, ValuedFeatures):
        msg = f"System {system_obj.name!r} does not expose valued features."
        raise NotImplementedError(msg)
    return representation


def _signature_is_unique(
    rows: Mapping[str, Mapping[str, object]],
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


def _select_minimal_columns(rows: Mapping[str, Mapping[str, object]]) -> tuple[str, ...]:
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
    query: frozenset[str] | Mapping[str, FeatureState | str],
    *,
    system: str | None = None,
    exact: bool = False,
    valued_dot_policy: Literal[
        "strict",
        "query-wildcard",
        "target-wildcard",
        "either-wildcard",
    ] = "strict",
) -> list[str]:
    """Return all graphemes that satisfy the requested feature query."""
    system_obj = get_system(system)
    found: list[str] = []

    if system_obj.representation_kind == "valued":
        if not isinstance(query, Mapping):
            msg = f"System {system_obj.name!r} requires dict-valued feature queries."
            raise NotImplementedError(msg)
        normalized_query = _normalize_valued_query(query)
        for grapheme in system_obj.list_graphemes():
            representation = system_obj.grapheme_to_representation(grapheme)
            if not isinstance(representation, ValuedFeatures):
                continue
            matched = (
                representation.values == normalized_query
                if exact
                else valued_matches(
                    normalized_query,
                    representation.values,
                    dot_policy=valued_dot_policy,
                )
            )
            if matched:
                found.append(grapheme)
        return found

    if not isinstance(query, frozenset):
        msg = f"System {system_obj.name!r} requires frozenset categorical queries."
        raise NotImplementedError(msg)

    for grapheme in system_obj.list_graphemes():
        features = system_obj.grapheme_to_features(grapheme)
        if features is None:
            continue

        matched = features == query if exact else system_obj.partial_match(query, features)
        if matched:
            found.append(grapheme)

    return found


def derive_class_features(
    graphemes: list[str] | tuple[str, ...],
    *,
    system: str | None = None,
) -> frozenset[str] | dict[str, FeatureState]:
    """Derive the strict shared feature intersection of a grapheme set."""
    if not graphemes:
        msg = "Cannot derive class features from an empty grapheme set."
        raise ValueError(msg)

    system_obj = get_system(system)

    if system_obj.representation_kind == "valued":
        valued_rows = [_lookup_valued(grapheme, system_obj).values for grapheme in graphemes]
        common_keys = set(valued_rows[0])
        for row in valued_rows[1:]:
            common_keys &= row.keys()
        shared = {
            key: valued_rows[0][key]
            for key in sorted(common_keys)
            if all(row[key] == valued_rows[0][key] for row in valued_rows[1:])
        }
        return shared

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

    if system_obj.representation_kind == "valued":
        valued_rows = {
            grapheme: dict(_lookup_valued(grapheme, system_obj).values)
            for grapheme in graphemes
        }
        columns = _select_minimal_columns(valued_rows)
        rows: dict[str, tuple[object, ...]] = {
            grapheme: tuple(
                valued_rows[grapheme].get(column, FeatureState.DOT)
                for column in columns
            )
            for grapheme in graphemes
        }
        return FeatureMatrix(columns=columns, rows=rows, system=system_name, mode="valued")

    if system_name == "distinctive" and hasattr(system_obj, "grapheme_to_scalars"):
        scalar_rows: dict[str, dict[str, object]] = {}
        for grapheme in graphemes:
            scalars = system_obj.grapheme_to_scalars(grapheme)
            if scalars is None:
                msg = f"Unsupported grapheme for scalar matrix: {grapheme!r}"
                raise KeyError(msg)
            scalar_rows[grapheme] = {
                name: value for name, value in scalars.items() if value != 0.0
            }

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
    if isinstance(value, FeatureState):
        return value.value
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
    format: str = "plain",  # noqa: A002
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
    valued_dot_policy: Literal["ignore", "partial", "strict"] = "ignore",
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
    representation_a = _lookup_representation(grapheme_a, system_obj)
    representation_b = _lookup_representation(grapheme_b, system_obj)
    if (
        isinstance(representation_a, ValuedFeatures)
        and isinstance(representation_b, ValuedFeatures)
    ):
        return valued_distance(
            representation_a.values,
            representation_b.values,
            dot_policy=valued_dot_policy,
        )
    return system_obj.segment_distance(representation_a, representation_b)


def valued_matches(
    query: Mapping[str, FeatureState | str],
    target: Mapping[str, FeatureState | str],
    *,
    dot_policy: Literal[
        "strict",
        "query-wildcard",
        "target-wildcard",
        "either-wildcard",
    ] = "strict",
) -> bool:
    """Match valued features with explicit DOT-state semantics."""
    normalized_query = _normalize_valued_query(query)
    normalized_target = _normalize_valued_query(target)

    for key, query_state in normalized_query.items():
        target_state = normalized_target.get(key, FeatureState.DOT)

        if dot_policy == "query-wildcard" and query_state == FeatureState.DOT:
            continue
        if dot_policy == "target-wildcard" and target_state == FeatureState.DOT:
            continue
        if dot_policy == "either-wildcard" and (
            query_state == FeatureState.DOT or target_state == FeatureState.DOT
        ):
            continue
        if query_state != target_state:
            return False

    return True


def valued_distance(
    a: Mapping[str, FeatureState | str],
    b: Mapping[str, FeatureState | str],
    *,
    dot_policy: Literal["ignore", "partial", "strict"] = "ignore",
) -> float:
    """Distance between valued feature bundles with configurable DOT handling.

    When *dot_policy* is ``"ignore"`` (the default), feature dimensions where
    either side is DOT are skipped entirely.  If **all** dimensions are skipped
    the function returns ``0.0``, meaning two fully-unspecified bundles are
    treated as identical.  This is mathematically consistent (no evidence of
    difference), but may surprise callers comparing nearly-empty P-base entries.
    Use ``"partial"`` or ``"strict"`` when unspecified dimensions should
    contribute to the distance.
    """
    a_values = _normalize_valued_query(a)
    b_values = _normalize_valued_query(b)

    keys = sorted(set(a_values) | set(b_values))
    if not keys:
        return 0.0

    total = 0.0
    comparable = 0

    for key in keys:
        left = a_values.get(key, FeatureState.DOT)
        right = b_values.get(key, FeatureState.DOT)

        if dot_policy == "ignore":
            if left == FeatureState.DOT or right == FeatureState.DOT:
                continue
            comparable += 1
            total += 0.0 if left == right else 1.0
            continue

        comparable += 1
        if dot_policy == "partial":
            if left == FeatureState.DOT and right == FeatureState.DOT:
                total += 0.0
            elif left == FeatureState.DOT or right == FeatureState.DOT:
                total += 0.5
            else:
                total += 0.0 if left == right else 1.0
            continue

        total += 0.0 if left == right else 1.0

    return (total / comparable) if comparable > 0 else 0.0
