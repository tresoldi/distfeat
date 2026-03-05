"""Tests for the Tresoldi feature system."""

from distfeat import TresoldiFeatureSystem, load_builtin_dataset


def test_tresoldi_lookup() -> None:
    """The Tresoldi system resolves common graphemes."""
    system = TresoldiFeatureSystem(dataset=load_builtin_dataset())
    features = system.grapheme_to_features("a")
    assert features is not None
    assert "vowel" in features


def test_tresoldi_class_lookup() -> None:
    """The Tresoldi system resolves sound classes."""
    system = TresoldiFeatureSystem(dataset=load_builtin_dataset())
    assert system.is_class("V") is True
