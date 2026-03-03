"""Tests for dataset APIs."""

from distfeat import dataset_from_rows, load_builtin_dataset


def test_load_builtin_dataset() -> None:
    """The bundled dataset loads core tables."""
    dataset = load_builtin_dataset()
    assert "a" in dataset.sounds
    assert "V" in dataset.classes
    assert len(dataset.features) > 100


def test_dataset_properties() -> None:
    """Computed dataset views expose expected derived structures."""
    dataset = load_builtin_dataset()
    assert "manner" in dataset.feature_values
    assert "V" in dataset.class_graphemes
    assert "V" in dataset.class_features


def test_dataset_from_rows() -> None:
    """Datasets can be created from in-memory rows."""
    dataset = dataset_from_rows(
        sounds={"a": "open front vowel"},
        classes={"V": ("vowel", "vowel", ["a"])},
        features=[("open", "height"), ("front", "centrality")],
    )
    assert dataset.sounds["a"] == "open front vowel"
    assert dataset.class_features["V"] == "vowel"
