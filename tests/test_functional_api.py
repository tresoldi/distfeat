"""Tests for top-level functional helpers."""

from distfeat import get_class_features, get_features, list_systems


def test_get_features() -> None:
    """Top-level helpers resolve grapheme features."""
    features = get_features("a")
    assert features is not None
    assert "vowel" in features


def test_get_class_features() -> None:
    """Top-level helpers resolve sound-class features."""
    features = get_class_features("V")
    assert features is not None
    assert "vowel" in features


def test_list_systems() -> None:
    """Built-in systems are registered in the global registry."""
    systems = list_systems()
    assert "ipa" in systems
