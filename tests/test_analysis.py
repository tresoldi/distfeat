"""Tests for the analysis helper APIs."""

import pytest

from distfeat import (
    FeatureMatrix,
    FeatureState,
    derive_class_features,
    distance,
    features_to_graphemes,
    get_system,
    minimal_matrix,
    tabulate_matrix,
    valued_distance,
    valued_matches,
)


def test_features_to_graphemes_partial() -> None:
    """Partial queries should return matching graphemes."""
    matches = features_to_graphemes(frozenset({"vowel"}))
    assert "a" in matches
    assert "p" not in matches


def test_features_to_graphemes_negative_query() -> None:
    """Negative feature queries should honor partial-match semantics."""
    matches = features_to_graphemes(frozenset({"consonant", "-voiced"}))
    assert "p" in matches
    assert "b" not in matches


def test_features_to_graphemes_exact() -> None:
    """Exact queries should only return exact feature matches."""
    system = get_system("ipa")
    features = system.grapheme_to_features("a")
    assert features is not None
    matches = features_to_graphemes(features, exact=True)
    assert "a" in matches


def test_derive_class_features() -> None:
    """Derived class features should be the strict feature intersection."""
    features = derive_class_features(["t", "d"])
    assert "consonant" in features
    assert "alveolar" in features
    assert "stop" in features
    assert "voiced" not in features


def test_minimal_matrix_categorical() -> None:
    """Categorical systems should yield a boolean feature matrix."""
    matrix = minimal_matrix(["t", "d"], system="ipa")
    assert isinstance(matrix, FeatureMatrix)
    assert matrix.mode == "categorical"
    assert matrix.columns == ("voiced",)
    assert matrix.rows["t"] == (False,)
    assert matrix.rows["d"] == (True,)


def test_minimal_matrix_distinctive() -> None:
    """The distinctive system should produce a scalar matrix."""
    matrix = minimal_matrix(["t", "d"], system="distinctive")
    assert isinstance(matrix, FeatureMatrix)
    assert matrix.mode == "scalar"
    assert matrix.columns
    assert all(isinstance(value, float) for value in matrix.rows["t"])


def test_tabulate_matrix_plain() -> None:
    """Plain-text matrix rendering should include a header and rows."""
    matrix = minimal_matrix(["t", "d"], system="ipa")
    rendered = tabulate_matrix(matrix)
    assert "grapheme" in rendered
    assert "t" in rendered
    assert "d" in rendered


def test_tabulate_matrix_markdown() -> None:
    """Markdown rendering should include a markdown separator row."""
    matrix = minimal_matrix(["t", "d"], system="ipa")
    rendered = tabulate_matrix(matrix, format="markdown")
    assert " | " in rendered
    assert "---" in rendered


def test_tabulate_matrix_invalid_format() -> None:
    """Unsupported formats should fail explicitly."""
    matrix = minimal_matrix(["t", "d"], system="ipa")
    with pytest.raises(NotImplementedError):
        tabulate_matrix(matrix, format="csv")


def test_distance_helper() -> None:
    """The helper should resolve graphemes and compute system distance."""
    assert distance("a", "a") == 0.0
    assert distance("a", "e") >= 0.0


def test_distance_precomputed() -> None:
    """Precomputed distance data should override system lookup."""
    matrix = {"a": {"e": 1.5}}
    assert distance("a", "e", precomputed=matrix) == 1.5
    assert distance("e", "a", precomputed=matrix) == 1.5


def test_distance_precomputed_missing_pair() -> None:
    """Missing precomputed entries should fail explicitly."""
    with pytest.raises(KeyError):
        distance("a", "u", precomputed={"a": {"e": 1.5}})


def test_features_to_graphemes_pbase_partial() -> None:
    """Valued systems should support dict-based partial queries."""
    matches = features_to_graphemes({"syllabic": "+"}, system="pbase-hc")
    assert "a" in matches
    assert "p" not in matches


def test_features_to_graphemes_pbase_exact() -> None:
    """Valued systems should support exact native-state matching."""
    system = get_system("pbase-hc")
    representation = system.grapheme_to_representation("a")
    assert representation is not None
    matches = features_to_graphemes(representation.values, system="pbase-hc", exact=True)
    assert "a" in matches


def test_derive_class_features_pbase() -> None:
    """Valued systems should derive shared multi-state features."""
    features = derive_class_features(["t", "d"], system="pbase-hc")
    assert isinstance(features, dict)
    assert features["consonantal"] == FeatureState.POSITIVE
    assert "voice" not in features


def test_minimal_matrix_pbase() -> None:
    """P-base systems should yield valued feature matrices."""
    matrix = minimal_matrix(["t", "d"], system="pbase-hc")
    assert isinstance(matrix, FeatureMatrix)
    assert matrix.mode == "valued"
    assert matrix.columns == ("voice",)
    assert matrix.rows["t"] == (FeatureState.NEGATIVE,)
    assert matrix.rows["d"] == (FeatureState.POSITIVE,)


def test_tabulate_matrix_pbase() -> None:
    """Valued matrix rendering should preserve symbolic feature states."""
    matrix = minimal_matrix(["t", "d"], system="pbase-hc")
    rendered = tabulate_matrix(matrix)
    assert "+" in rendered
    assert "-" in rendered


def test_distance_helper_pbase() -> None:
    """The distance helper should use native multi-state distances."""
    assert distance("a", "a", system="pbase-hc") == 0.0
    assert distance("t", "d", system="pbase-hc") > 0.0


def test_valued_matches_dot_policies() -> None:
    """DOT handling in valued matching should be configurable."""
    query = {"syllabic": FeatureState.DOT, "voice": FeatureState.POSITIVE}
    target = {"syllabic": FeatureState.NEGATIVE, "voice": FeatureState.POSITIVE}
    assert valued_matches(query, target, dot_policy="strict") is False
    assert valued_matches(query, target, dot_policy="query-wildcard") is True
    assert valued_matches(query, target, dot_policy="either-wildcard") is True


def test_valued_distance_dot_policies() -> None:
    """DOT handling in valued distance should be configurable."""
    left = {"syllabic": FeatureState.DOT, "voice": FeatureState.POSITIVE}
    right = {"syllabic": FeatureState.NEGATIVE, "voice": FeatureState.POSITIVE}
    assert valued_distance(left, right, dot_policy="ignore") == 0.0
    assert valued_distance(left, right, dot_policy="partial") == 0.25
    assert valued_distance(left, right, dot_policy="strict") == 0.5


def test_features_to_graphemes_valued_dot_policy() -> None:
    """Valued grapheme queries should support wildcard DOT policies."""
    strict = features_to_graphemes(
        {"syllabic": ".", "vocalic": "+"},
        system="pbase-hc",
        valued_dot_policy="strict",
    )
    wildcard = features_to_graphemes(
        {"syllabic": ".", "vocalic": "+"},
        system="pbase-hc",
        valued_dot_policy="query-wildcard",
    )
    assert len(wildcard) >= len(strict)
    assert "a" in wildcard
