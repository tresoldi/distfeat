"""Public API for the distfeat package."""

__version__ = "0.4.0"

from distfeat.analysis import (
    FeatureMatrix,
    derive_class_features,
    distance,
    features_to_graphemes,
    minimal_matrix,
    tabulate_matrix,
)
from distfeat.dataset import FeatureDataset, dataset_from_rows, load_builtin_dataset, load_dataset
from distfeat.exporters import export_class_features, export_distances, export_matrix
from distfeat.geometry import DEFAULT_GEOMETRY, FeatureNode, GeometryNode
from distfeat.protocol import FeatureSystem
from distfeat.registry import (
    Registry,
    add_features,
    create_registry,
    feature_distance,
    features_to_grapheme,
    get_class_features,
    get_class_representation,
    get_features,
    get_registry,
    get_representation,
    get_system,
    is_class,
    list_systems,
    matches,
    partial_match,
    register,
    reset_registry,
    segment_distance,
    set_default,
    set_registry,
    sound_distance,
)
from distfeat.representations import (
    CategoricalFeatures,
    FeatureRepresentation,
    FeatureState,
    ValuedFeatures,
)
from distfeat.systems.distinctive import DistinctiveFeatureSystem
from distfeat.systems.ipa import IPAFeatureSystem
from distfeat.systems.pbase import PBaseFeatureSystem
from distfeat.systems.tresoldi import TresoldiFeatureSystem

__all__ = [
    "__version__",
    "DEFAULT_GEOMETRY",
    "DistinctiveFeatureSystem",
    "CategoricalFeatures",
    "FeatureDataset",
    "FeatureMatrix",
    "FeatureNode",
    "FeatureRepresentation",
    "FeatureState",
    "FeatureSystem",
    "GeometryNode",
    "IPAFeatureSystem",
    "PBaseFeatureSystem",
    "Registry",
    "TresoldiFeatureSystem",
    "ValuedFeatures",
    "add_features",
    "create_registry",
    "dataset_from_rows",
    "derive_class_features",
    "distance",
    "feature_distance",
    "export_class_features",
    "export_distances",
    "export_matrix",
    "features_to_grapheme",
    "features_to_graphemes",
    "get_class_features",
    "get_class_representation",
    "get_features",
    "get_registry",
    "get_representation",
    "get_system",
    "is_class",
    "list_systems",
    "matches",
    "load_builtin_dataset",
    "load_dataset",
    "minimal_matrix",
    "partial_match",
    "register",
    "reset_registry",
    "segment_distance",
    "set_default",
    "set_registry",
    "sound_distance",
    "tabulate_matrix",
]
