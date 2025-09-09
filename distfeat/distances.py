"""
Phonetic distance calculation methods.

Provides various distance metrics for comparing phonemes and building distance matrices.
"""

import logging
from functools import lru_cache
from typing import Callable, Dict, List, Optional, Tuple, Union
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances

from .features import phoneme_to_features, get_feature_system, get_feature_names

logger = logging.getLogger('distfeat')

# Registry of distance methods
_DISTANCE_METHODS: Dict[str, Callable] = {}


def register_distance_method(name: str, func: Callable) -> None:
    """
    Register a custom distance method.
    
    Args:
        name: Name for the distance method
        func: Function that takes two feature vectors and returns a distance
    """
    _DISTANCE_METHODS[name] = func
    logger.info(f"Registered distance method: {name}")


@lru_cache(maxsize=4096)
def calculate_distance(
    phoneme1: str,
    phoneme2: str,
    method: str = 'hamming',
    normalize: bool = True,
    on_error: str = 'warn',
    **kwargs
) -> Optional[float]:
    """
    Calculate distance between two phonemes.
    
    Args:
        phoneme1: First phoneme
        phoneme2: Second phoneme  
        method: Distance method ('hamming', 'jaccard', 'euclidean', 'cosine', 'manhattan', 'kmeans')
        normalize: Normalize distance to [0, 1] range
        on_error: Error handling - 'raise', 'warn', or 'ignore'
        **kwargs: Additional arguments for specific methods
        
    Returns:
        Distance value, or None if phonemes not found
    """
    # Get feature vectors
    features1 = phoneme_to_features(phoneme1, on_error=on_error)
    features2 = phoneme_to_features(phoneme2, on_error=on_error)
    
    if features1 is None or features2 is None:
        return None
    
    # Convert to arrays
    feature_names = get_feature_names()
    vec1 = np.array([features1.get(f, 0) for f in feature_names])
    vec2 = np.array([features2.get(f, 0) for f in feature_names])
    
    # Calculate distance
    if method == 'hamming':
        dist = _hamming_distance(vec1, vec2, normalize)
    elif method == 'jaccard':
        dist = _jaccard_distance(vec1, vec2)
    elif method == 'euclidean':
        dist = _euclidean_distance(vec1, vec2, normalize)
    elif method == 'cosine':
        dist = _cosine_distance(vec1, vec2)
    elif method == 'manhattan':
        dist = _manhattan_distance(vec1, vec2, normalize)
    elif method == 'kmeans':
        n_clusters = kwargs.get('n_clusters', 12)
        dist = _kmeans_distance(phoneme1, phoneme2, n_clusters)
    elif method in _DISTANCE_METHODS:
        dist = _DISTANCE_METHODS[method](vec1, vec2)
        if normalize and method not in ['jaccard', 'cosine']:
            dist = dist / len(vec1)
    else:
        raise ValueError(f"Unknown distance method: {method}")
    
    return float(dist)


def build_distance_matrix(
    phonemes: Optional[List[str]] = None,
    method: str = 'hamming',
    normalize: bool = True,
    n_clusters: Optional[int] = None,
    cache: bool = True
) -> Tuple[np.ndarray, List[str]]:
    """
    Build a distance matrix for a set of phonemes.
    
    Args:
        phonemes: List of phonemes (None for all in system)
        method: Distance method to use
        normalize: Normalize distances to [0, 1]
        n_clusters: Number of clusters for k-means method
        cache: Cache distance calculations
        
    Returns:
        Tuple of (distance matrix, phoneme list)
    """
    # Get phoneme list
    if phonemes is None:
        feature_system = get_feature_system()
        phonemes = sorted(feature_system.keys())
    
    n = len(phonemes)
    matrix = np.zeros((n, n))
    
    if method == 'kmeans':
        # Special handling for k-means clustering
        matrix = _build_kmeans_matrix(phonemes, n_clusters or 12)
    else:
        # Calculate pairwise distances
        for i in range(n):
            for j in range(i + 1, n):
                if cache:
                    dist = calculate_distance(
                        phonemes[i], phonemes[j], 
                        method=method, normalize=normalize
                    )
                else:
                    # Direct calculation without caching
                    dist = _calculate_distance_uncached(
                        phonemes[i], phonemes[j],
                        method, normalize
                    )
                
                if dist is not None:
                    matrix[i, j] = matrix[j, i] = dist
                else:
                    # Use maximum distance for missing phonemes
                    matrix[i, j] = matrix[j, i] = 1.0 if normalize else np.inf
    
    return matrix, phonemes


def available_distance_methods() -> List[str]:
    """Get list of available distance methods."""
    builtin = ['hamming', 'jaccard', 'euclidean', 'cosine', 'manhattan', 'kmeans']
    custom = list(_DISTANCE_METHODS.keys())
    return builtin + custom


# Distance calculation functions

def _hamming_distance(vec1: np.ndarray, vec2: np.ndarray, normalize: bool) -> float:
    """Hamming distance (number of differing features)."""
    dist = np.sum(vec1 != vec2)
    if normalize:
        dist = dist / len(vec1)
    return dist


def _jaccard_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Jaccard distance (1 - Jaccard similarity)."""
    intersection = np.sum((vec1 == 1) & (vec2 == 1))
    union = np.sum((vec1 == 1) | (vec2 == 1))
    
    if union == 0:
        return 0.0
    
    return 1.0 - (intersection / union)


def _euclidean_distance(vec1: np.ndarray, vec2: np.ndarray, normalize: bool) -> float:
    """Euclidean distance."""
    dist = np.linalg.norm(vec1 - vec2)
    if normalize:
        # Normalize by maximum possible distance
        max_dist = np.sqrt(len(vec1))
        dist = dist / max_dist
    return dist


def _cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Cosine distance (1 - cosine similarity)."""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 1.0
    
    similarity = dot_product / (norm1 * norm2)
    distance = 1.0 - similarity
    
    # Handle floating point precision for identical vectors
    if np.array_equal(vec1, vec2):
        return 0.0
    
    return max(0.0, distance)  # Ensure non-negative


def _manhattan_distance(vec1: np.ndarray, vec2: np.ndarray, normalize: bool) -> float:
    """Manhattan (L1) distance."""
    dist = np.sum(np.abs(vec1 - vec2))
    if normalize:
        dist = dist / len(vec1)
    return dist


def _build_kmeans_matrix(phonemes: List[str], n_clusters: int) -> np.ndarray:
    """Build distance matrix using k-means clustering."""
    # Get feature vectors for all phonemes
    feature_system = get_feature_system()
    feature_names = get_feature_names()
    
    vectors = []
    valid_phonemes = []
    
    for phoneme in phonemes:
        if phoneme in feature_system:
            features = feature_system[phoneme]['features']
            vec = [features.get(f, 0) for f in feature_names]
            vectors.append(vec)
            valid_phonemes.append(phoneme)
    
    if not vectors:
        return np.zeros((len(phonemes), len(phonemes)))
    
    # Perform k-means clustering
    X = np.array(vectors)
    kmeans = KMeans(n_clusters=min(n_clusters, len(valid_phonemes)), 
                    random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_
    
    # Build distance matrix based on centroid distances
    n = len(phonemes)
    matrix = np.zeros((n, n))
    
    # Create phoneme to cluster mapping
    phoneme_to_cluster = {p: c for p, c in zip(valid_phonemes, clusters)}
    
    for i, p1 in enumerate(phonemes):
        for j, p2 in enumerate(phonemes):
            if i == j:
                continue
                
            if p1 in phoneme_to_cluster and p2 in phoneme_to_cluster:
                c1 = phoneme_to_cluster[p1]
                c2 = phoneme_to_cluster[p2]
                dist = np.linalg.norm(centroids[c1] - centroids[c2])
                # Normalize to [0, 1]
                max_dist = np.max(pairwise_distances(centroids))
                if max_dist > 0:
                    dist = dist / max_dist
                matrix[i, j] = dist
            else:
                # Use maximum distance for missing phonemes
                matrix[i, j] = 1.0
    
    return matrix


def _kmeans_distance(phoneme1: str, phoneme2: str, n_clusters: int) -> float:
    """Calculate distance using k-means clustering approach."""
    # This is a simplified version - in practice, we'd cache the clustering
    phonemes = [phoneme1, phoneme2]
    matrix, _ = build_distance_matrix(phonemes, method='kmeans', n_clusters=n_clusters)
    return matrix[0, 1]


def _calculate_distance_uncached(
    phoneme1: str, 
    phoneme2: str,
    method: str,
    normalize: bool
) -> Optional[float]:
    """Calculate distance without caching (internal use)."""
    # Get feature vectors
    features1 = phoneme_to_features(phoneme1, on_error='ignore')
    features2 = phoneme_to_features(phoneme2, on_error='ignore')
    
    if features1 is None or features2 is None:
        return None
    
    # Convert to arrays
    feature_names = get_feature_names()
    vec1 = np.array([features1.get(f, 0) for f in feature_names])
    vec2 = np.array([features2.get(f, 0) for f in feature_names])
    
    # Calculate distance based on method
    if method == 'hamming':
        return _hamming_distance(vec1, vec2, normalize)
    elif method == 'jaccard':
        return _jaccard_distance(vec1, vec2)
    elif method == 'euclidean':
        return _euclidean_distance(vec1, vec2, normalize)
    elif method == 'cosine':
        return _cosine_distance(vec1, vec2)
    elif method == 'manhattan':
        return _manhattan_distance(vec1, vec2, normalize)
    else:
        return None