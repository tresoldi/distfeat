"""Stable export helpers for common analysis outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import TYPE_CHECKING

from distfeat.representations import FeatureState

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from distfeat.analysis import FeatureMatrix


def _resolve_format(path: str | Path, format: str | None, *, allowed: set[str]) -> str:  # noqa: A002
    normalized = format.lower() if format is not None else Path(path).suffix.lstrip(".").lower()

    if normalized not in allowed:
        options = ", ".join(sorted(allowed))
        msg = f"Unsupported export format: {normalized!r}. Allowed: {options}"
        raise ValueError(msg)
    return normalized


def _serialize_value(value: object) -> str | float | int | bool | None:
    if isinstance(value, FeatureState):
        return value.value
    return value if isinstance(value, (str, float, int, bool)) else str(value)


def _write_delimited(
    path: Path,
    header: list[str],
    rows: Sequence[Sequence[object]],
    *,
    delimiter: str,
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter=delimiter)
        writer.writerow(header)
        writer.writerows(rows)


def export_matrix(
    matrix: FeatureMatrix,
    path: str | Path,
    *,
    format: str | None = None,  # noqa: A002
) -> Path:
    """Export a feature matrix to JSON, CSV, or TSV."""
    output_path = Path(path)
    normalized = _resolve_format(output_path, format, allowed={"json", "csv", "tsv"})

    header = ["grapheme", *matrix.columns]
    rows = [
        [grapheme, *[_serialize_value(value) for value in matrix.rows[grapheme]]]
        for grapheme in matrix.rows
    ]

    if normalized == "json":
        payload = {
            "system": matrix.system,
            "mode": matrix.mode,
            "columns": list(matrix.columns),
            "rows": [
                {
                    "grapheme": row[0],
                    "values": row[1:],
                }
                for row in rows
            ],
        }
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return output_path

    delimiter = "," if normalized == "csv" else "\t"
    _write_delimited(output_path, header, rows, delimiter=delimiter)
    return output_path


def export_distances(
    distances: Mapping[str, Mapping[str, float]],
    path: str | Path,
    *,
    format: str | None = None,  # noqa: A002
) -> Path:
    """Export a nested distance map to JSON, CSV, or TSV."""
    output_path = Path(path)
    normalized = _resolve_format(output_path, format, allowed={"json", "csv", "tsv"})

    sources = sorted(distances)
    if normalized == "json":
        payload: dict[str, object] = {
            source: {target: distances[source][target] for target in sorted(distances[source])}
            for source in sources
        }
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return output_path

    rows: list[list[object]] = []
    for source in sources:
        for target in sorted(distances[source]):
            rows.append([source, target, distances[source][target]])

    delimiter = "," if normalized == "csv" else "\t"
    _write_delimited(output_path, ["source", "target", "distance"], rows, delimiter=delimiter)
    return output_path


def export_class_features(
    features: frozenset[str] | Mapping[str, FeatureState | str],
    path: str | Path,
    *,
    format: str | None = None,  # noqa: A002
) -> Path:
    """Export class-feature output to JSON, CSV, or TSV."""
    output_path = Path(path)
    normalized = _resolve_format(output_path, format, allowed={"json", "csv", "tsv"})

    if isinstance(features, frozenset):
        if normalized == "json":
            categorical_payload: dict[str, object] = {
                "kind": "categorical",
                "features": sorted(features),
            }
            output_path.write_text(
                json.dumps(categorical_payload, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
            return output_path

        rows = [[feature] for feature in sorted(features)]
        delimiter = "," if normalized == "csv" else "\t"
        _write_delimited(output_path, ["feature"], rows, delimiter=delimiter)
        return output_path

    normalized_values = {
        key: value.value if isinstance(value, FeatureState) else str(value)
        for key, value in features.items()
    }

    if normalized == "json":
        valued_payload: dict[str, object] = {
            "kind": "valued",
            "features": {key: normalized_values[key] for key in sorted(normalized_values)},
        }
        output_path.write_text(
            json.dumps(valued_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return output_path

    rows = [[key, normalized_values[key]] for key in sorted(normalized_values)]
    delimiter = "," if normalized == "csv" else "\t"
    _write_delimited(output_path, ["feature", "state"], rows, delimiter=delimiter)
    return output_path
