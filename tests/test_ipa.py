"""Tests for the IPA feature system."""

from distfeat import IPAFeatureSystem, load_builtin_dataset


def test_ipa_lookup() -> None:
    """The IPA system resolves common graphemes."""
    system = IPAFeatureSystem(dataset=load_builtin_dataset())
    features = system.grapheme_to_features("a")
    assert features is not None
    assert "vowel" in features


def test_ipa_class_lookup() -> None:
    """The IPA system resolves sound classes."""
    system = IPAFeatureSystem(dataset=load_builtin_dataset())
    features = system.class_features("V")
    assert features is not None
    assert "vowel" in features
