"""Public API for the distfeat package."""

__version__ = "0.3.0"

from distfeat.analysis import (
    FeatureMatrix,
    derive_class_features,
    distance,
    features_to_graphemes,
    minimal_matrix,
    tabulate_matrix,
)
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
    "__version__",
    "DEFAULT_GEOMETRY",
    "DistinctiveFeatureSystem",
    "FeatureDataset",
    "FeatureMatrix",
    "FeatureNode",
    "FeatureSystem",
    "GeometryNode",
    "IPAFeatureSystem",
    "Registry",
    "TresoldiFeatureSystem",
    "add_features",
    "create_registry",
    "dataset_from_rows",
    "derive_class_features",
    "distance",
    "feature_distance",
    "features_to_grapheme",
    "features_to_graphemes",
    "get_class_features",
    "get_features",
    "get_registry",
    "get_system",
    "is_class",
    "list_systems",
    "load_builtin_dataset",
    "load_dataset",
    "minimal_matrix",
    "partial_match",
    "register",
    "reset_registry",
    "set_default",
    "set_registry",
    "sound_distance",
    "tabulate_matrix",
]
