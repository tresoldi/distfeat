"""Public API for the distfeat package."""

from distfeat.dataset import FeatureDataset, dataset_from_rows, load_builtin_dataset, load_dataset
from distfeat.geometry import DEFAULT_GEOMETRY, FeatureNode, GeometryNode
from distfeat.protocol import FeatureSystem
from distfeat.registry import (
    Registry,
    add_features,
    create_registry,
    feature_distance,
    features_to_grapheme,
    get_class_features,
    get_features,
    get_registry,
    get_system,
    is_class,
    list_systems,
    partial_match,
    register,
    reset_registry,
    set_default,
    set_registry,
    sound_distance,
)
from distfeat.systems.distinctive import DistinctiveFeatureSystem
from distfeat.systems.ipa import IPAFeatureSystem
from distfeat.systems.tresoldi import TresoldiFeatureSystem

__all__ = [
    "DEFAULT_GEOMETRY",
    "DistinctiveFeatureSystem",
    "FeatureDataset",
    "FeatureNode",
    "FeatureSystem",
    "GeometryNode",
    "IPAFeatureSystem",
    "Registry",
    "TresoldiFeatureSystem",
    "add_features",
    "create_registry",
    "dataset_from_rows",
    "feature_distance",
    "features_to_grapheme",
    "get_class_features",
    "get_features",
    "get_registry",
    "get_system",
    "is_class",
    "list_systems",
    "load_builtin_dataset",
    "load_dataset",
    "partial_match",
    "register",
    "reset_registry",
    "set_default",
    "set_registry",
    "sound_distance",
]
