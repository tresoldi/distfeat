"""
distfeat: A Phonetic Distance and Feature Library for Computational Historical Linguistics.

A comprehensive library for phonetic feature extraction and distance calculation,
designed for computational historical linguistics research. Provides binary feature 
vectors for IPA phonemes, multiple distance metrics, and validation tools.
"""

__version__ = "0.2.0"

# Core feature functions
from .features import (
    phoneme_to_features,
    features_to_phoneme,
    get_feature_system,
    get_feature_names,
    load_custom_features,
)

# Distance calculation functions
from .distances import (
    calculate_distance,
    build_distance_matrix,
    available_distance_methods,
    register_distance_method,
)

# Normalization utilities
from .normalization import (
    normalize_glyph,
    normalize_ipa,
    canonicalize_ipa,
)

# I/O utilities
from .io import (
    save_distance_matrix,
    load_distance_matrix,
    export_matrix_tsv,
    export_matrix_csv,
    export_matrix_json,
)

# Configuration
from .config import (
    get_config,
    set_config,
    load_config,
)

__all__ = [
    "__version__",
    # Features
    "phoneme_to_features",
    "features_to_phoneme",
    "get_feature_system",
    "get_feature_names",
    "load_custom_features",
    # Distances
    "calculate_distance",
    "build_distance_matrix",
    "available_distance_methods",
    "register_distance_method",
    # Normalization
    "normalize_glyph",
    "normalize_ipa",
    "canonicalize_ipa",
    # I/O
    "save_distance_matrix",
    "load_distance_matrix",
    "export_matrix_tsv",
    "export_matrix_csv",
    "export_matrix_json",
    # Config
    "get_config",
    "set_config",
    "load_config",
]