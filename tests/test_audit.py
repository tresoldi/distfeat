"""Tests for dataset audit utilities."""

from distfeat import audit_dataset, dataset_from_rows, load_builtin_dataset


def test_audit_builtin_dataset_reports_basic_counts() -> None:
    """The bundled dataset should produce a valid high-level report."""
    report = audit_dataset(load_builtin_dataset())
    assert report.sound_count > 0
    assert report.class_count > 0
    assert report.feature_pair_count > 0
    assert 0.0 <= report.class_reference_coverage <= 1.0


def test_audit_detects_unknown_and_duplicate_references() -> None:
    """Audit should detect unknown graphemes/features and duplicate class members."""
    dataset = dataset_from_rows(
        sounds={"a": "open front vowel", "b": "voiced bilabial stop"},
        classes={
            "X": ("bad class", "vowel,-imaginary", ["a", "a", "z"]),
        },
        features=[
            ("vowel", "type"),
            ("vowel", "manner"),
            ("voiced", "phonation"),
        ],
    )
    report = audit_dataset(dataset)
    assert report.has_issues is True
    assert report.unknown_class_graphemes["X"] == ("z",)
    assert report.duplicate_class_graphemes["X"] == ("a",)
    assert report.unknown_class_features["X"] == ("imaginary",)
    assert report.feature_value_conflicts["vowel"] == ("manner", "type")
    assert "b" in report.unreferenced_sounds
