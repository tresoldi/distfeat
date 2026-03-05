"""Tests for the distinctive feature system."""

from distfeat import DistinctiveFeatureSystem, load_builtin_dataset


def test_distinctive_lookup() -> None:
    """The distinctive system resolves common graphemes."""
    system = DistinctiveFeatureSystem(dataset=load_builtin_dataset())
    features = system.grapheme_to_features("a")
    assert features is not None
    assert "vowel" in features


def test_distinctive_scalars() -> None:
    """The distinctive system exposes scalar conversion."""
    system = DistinctiveFeatureSystem(dataset=load_builtin_dataset())
    scalars = system.grapheme_to_scalars("a")
    assert scalars is not None
    assert isinstance(scalars, dict)
