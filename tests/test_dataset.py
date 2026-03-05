"""Tests for dataset APIs."""

import pickle

import pytest

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


def test_dataset_is_deeply_immutable() -> None:
    """FeatureDataset should not expose mutable nested state."""
    sounds = {"a": "open front vowel"}
    classes = {"V": ("vowel", "vowel", ["a"])}
    features = [("open", "height"), ("front", "centrality")]

    dataset = dataset_from_rows(sounds=sounds, classes=classes, features=features)

    sounds["a"] = "mutated"
    classes["V"][2].append("e")
    features.append(("back", "centrality"))

    assert dataset.sounds["a"] == "open front vowel"
    assert dataset.class_graphemes["V"] == frozenset({"a"})
    assert dataset.features == (("open", "height"), ("front", "centrality"))

    with pytest.raises(TypeError):
        dataset.sounds["a"] = "x"  # type: ignore[index]
    with pytest.raises(TypeError):
        dataset.classes["V"] = ("vowel", "vowel", ("a",))  # type: ignore[index]
    with pytest.raises(TypeError):
        dataset.features[0] = ("open", "height")  # type: ignore[index]


def test_dataset_pickle_roundtrip_preserves_immutability() -> None:
    """FeatureDataset should remain pickleable while deeply immutable."""
    dataset = load_builtin_dataset()
    restored = pickle.loads(pickle.dumps(dataset))

    assert restored.sounds == dataset.sounds
    assert restored.classes == dataset.classes
    assert restored.features == dataset.features

    with pytest.raises(TypeError):
        restored.sounds["a"] = "x"  # type: ignore[index]
