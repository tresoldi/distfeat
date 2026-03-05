"""Tests for native representation types."""

import pytest

from distfeat import FeatureState, ValuedFeatures


def test_valued_features_is_immutable() -> None:
    """ValuedFeatures should defensively copy and expose immutable mappings."""
    values = {"syllabic": FeatureState.POSITIVE}
    representation = ValuedFeatures(values=values)

    values["syllabic"] = FeatureState.NEGATIVE
    assert representation.values["syllabic"] == FeatureState.POSITIVE

    with pytest.raises(TypeError):
        representation.values["syllabic"] = FeatureState.NEGATIVE  # type: ignore[index]
