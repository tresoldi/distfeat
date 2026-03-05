"""Tests for export helpers."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from distfeat import (
    FeatureState,
    derive_class_features,
    export_class_features,
    export_distances,
    export_matrix,
    minimal_matrix,
)

if TYPE_CHECKING:
    from pathlib import Path


def test_export_matrix_json(tmp_path: Path) -> None:
    """Matrices should export as stable JSON."""
    matrix = minimal_matrix(["t", "d"], system="ipa")
    output = tmp_path / "matrix.json"
    result = export_matrix(matrix, output)
    assert result == output
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["system"] == "ipa"
    assert payload["columns"] == ["voiced"]
    assert payload["rows"][0]["grapheme"] == "t"


def test_export_distances_tsv(tmp_path: Path) -> None:
    """Distance maps should export to delimited tables."""
    output = tmp_path / "distances.tsv"
    export_distances({"a": {"e": 1.5, "i": 2.0}}, output)
    lines = output.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "source\ttarget\tdistance"
    assert lines[1] == "a\te\t1.5"
    assert lines[2] == "a\ti\t2.0"


def test_export_class_features_categorical_csv(tmp_path: Path) -> None:
    """Categorical class features should export one feature per row."""
    features = derive_class_features(["t", "d"], system="ipa")
    assert isinstance(features, frozenset)
    output = tmp_path / "class.csv"
    export_class_features(features, output)
    lines = output.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "feature"
    assert "consonant" in set(lines[1:])


def test_export_class_features_valued_json(tmp_path: Path) -> None:
    """Valued class features should preserve symbolic states in JSON."""
    features = {"consonantal": FeatureState.POSITIVE, "voice": FeatureState.NEGATIVE}
    output = tmp_path / "class.json"
    export_class_features(features, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["kind"] == "valued"
    assert payload["features"]["consonantal"] == "+"
    assert payload["features"]["voice"] == "-"
