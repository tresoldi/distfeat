"""
Unit and property-based tests for distance calculations.
"""

import pytest
import numpy as np
from distfeat import (
    calculate_distance,
    build_distance_matrix,
    available_distance_methods,
    register_distance_method
)


class TestDistanceCalculation:
    """Test basic distance calculations."""
    
    def test_identical_phonemes(self):
        """Test that identical phonemes have zero distance."""
        for method in ['hamming', 'jaccard', 'euclidean', 'cosine', 'manhattan']:
            dist = calculate_distance('p', 'p', method=method)
            assert dist == 0.0, f"Method {method} should give 0 for identical phonemes"
    
    def test_symmetry(self):
        """Test that distance is symmetric."""
        for method in available_distance_methods():
            if method == 'kmeans':
                continue  # K-means needs special handling
            
            dist_ab = calculate_distance('p', 'b', method=method)
            dist_ba = calculate_distance('b', 'p', method=method)
            
            assert dist_ab == dist_ba, f"Method {method} violates symmetry"
    
    def test_normalization(self):
        """Test that normalized distances are in [0, 1]."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'a', 'i', 'u']
        
        for method in ['hamming', 'euclidean', 'manhattan']:
            for i in range(len(phonemes)):
                for j in range(len(phonemes)):
                    dist = calculate_distance(
                        phonemes[i], phonemes[j], 
                        method=method, normalize=True
                    )
                    if dist is not None:
                        assert 0.0 <= dist <= 1.0, \
                            f"Method {method} gives out-of-range distance: {dist}"
    
    def test_triangle_inequality(self):
        """Test that distances satisfy triangle inequality."""
        phonemes = ['p', 'b', 't']
        
        for method in ['hamming', 'euclidean', 'manhattan']:
            dists = {}
            for i in range(len(phonemes)):
                for j in range(len(phonemes)):
                    dists[i, j] = calculate_distance(
                        phonemes[i], phonemes[j], 
                        method=method
                    )
            
            # Check triangle inequality: d(a,c) <= d(a,b) + d(b,c)
            for i in range(len(phonemes)):
                for j in range(len(phonemes)):
                    for k in range(len(phonemes)):
                        if None not in [dists[i, k], dists[i, j], dists[j, k]]:
                            assert dists[i, k] <= dists[i, j] + dists[j, k] + 1e-10, \
                                f"Triangle inequality violated for {method}"


class TestLinguisticPatterns:
    """Test that distances reflect linguistic patterns."""
    
    def test_voice_distinction(self):
        """Test voiced/voiceless pairs are close."""
        pairs = [('p', 'b'), ('t', 'd'), ('k', 'g'), ('f', 'v'), ('s', 'z')]
        
        for p1, p2 in pairs:
            dist = calculate_distance(p1, p2, method='hamming')
            if dist is not None:
                # Voice pairs should be close (differ in few features)
                assert dist < 0.3, f"Voice pair {p1}-{p2} too distant: {dist}"
    
    def test_place_of_articulation(self):
        """Test place of articulation series."""
        # Voiceless stops
        stops = ['p', 't', 'k']
        
        # Adjacent places should be closer than distant ones
        dist_pt = calculate_distance('p', 't')
        dist_tk = calculate_distance('t', 'k')
        dist_pk = calculate_distance('p', 'k')
        
        if all(d is not None for d in [dist_pt, dist_tk, dist_pk]):
            # p-k should be more distant than p-t or t-k
            assert dist_pk >= min(dist_pt, dist_tk), \
                "Place of articulation distances inconsistent"
    
    def test_manner_classes(self):
        """Test manner of articulation distinctions."""
        # Stops vs fricatives
        stops = ['p', 't', 'k']
        fricatives = ['f', 's', 'x']
        
        within_stop_dists = []
        within_fric_dists = []
        across_dists = []
        
        # Calculate within-class distances
        for i in range(len(stops)):
            for j in range(i + 1, len(stops)):
                dist = calculate_distance(stops[i], stops[j])
                if dist is not None:
                    within_stop_dists.append(dist)
                
                dist = calculate_distance(fricatives[i], fricatives[j])
                if dist is not None:
                    within_fric_dists.append(dist)
        
        # Calculate across-class distances
        for stop in stops:
            for fric in fricatives:
                dist = calculate_distance(stop, fric)
                if dist is not None:
                    across_dists.append(dist)
        
        # Within-class should be smaller than across-class on average
        if within_stop_dists and across_dists:
            avg_within = np.mean(within_stop_dists + within_fric_dists)
            avg_across = np.mean(across_dists)
            
            # This is a soft constraint - may not always hold
            # but should generally be true
            assert avg_within <= avg_across * 1.2, \
                "Manner classes not well separated"


class TestDistanceMatrix:
    """Test distance matrix construction."""
    
    def test_matrix_shape(self):
        """Test matrix has correct shape."""
        phonemes = ['p', 'b', 't', 'd']
        matrix, labels = build_distance_matrix(phonemes)
        
        assert matrix.shape == (len(phonemes), len(phonemes))
        assert len(labels) == len(phonemes)
        assert labels == phonemes
    
    def test_matrix_symmetry(self):
        """Test matrix is symmetric."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g']
        matrix, _ = build_distance_matrix(phonemes)
        
        assert np.allclose(matrix, matrix.T), "Distance matrix not symmetric"
    
    def test_matrix_diagonal(self):
        """Test diagonal is zero."""
        phonemes = ['a', 'e', 'i', 'o', 'u']
        matrix, _ = build_distance_matrix(phonemes)
        
        assert np.allclose(np.diag(matrix), 0), "Diagonal should be zero"
    
    def test_kmeans_matrix(self):
        """Test k-means clustering distance matrix."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g']
        matrix, labels = build_distance_matrix(
            phonemes, method='kmeans', n_clusters=3
        )
        
        assert matrix.shape == (len(phonemes), len(phonemes))
        assert np.allclose(matrix, matrix.T)
        assert np.allclose(np.diag(matrix), 0)
        
        # Check that matrix has expected clustering structure
        # (phonemes in same cluster should have 0 distance)
        unique_distances = np.unique(matrix)
        assert len(unique_distances) <= 4  # At most n_clusters + 1 unique values


class TestCustomDistances:
    """Test custom distance registration."""
    
    def test_register_custom(self):
        """Test registering custom distance function."""
        def manhattan_squared(vec1, vec2):
            return np.sum(np.abs(vec1 - vec2)) ** 2
        
        register_distance_method('manhattan_squared', manhattan_squared)
        
        assert 'manhattan_squared' in available_distance_methods()
        
        # Test using custom method
        dist = calculate_distance('p', 'b', method='manhattan_squared')
        assert dist is not None