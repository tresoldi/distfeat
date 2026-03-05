"""Tests for geometry APIs."""

from distfeat.geometry import DEFAULT_GEOMETRY, FeatureNode, GeometryNode


def test_root_geometry_node() -> None:
    """The default geometry tree has the expected root."""
    assert isinstance(DEFAULT_GEOMETRY, GeometryNode)
    assert DEFAULT_GEOMETRY.name == "Root"


def test_feature_lookup() -> None:
    """Known features resolve to leaf nodes."""
    node = DEFAULT_GEOMETRY.find_feature("voiced")
    assert isinstance(node, FeatureNode)
    assert node is not None
    assert node.name == "voice"


def test_feature_distance() -> None:
    """Feature distance is symmetric and zero on identity."""
    assert DEFAULT_GEOMETRY.feature_distance("voiced", "voiced") == 0
    left = DEFAULT_GEOMETRY.feature_distance("voiced", "voiceless")
    right = DEFAULT_GEOMETRY.feature_distance("voiceless", "voiced")
    assert left == right
