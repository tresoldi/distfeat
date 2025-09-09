"""
Integration tests with real phonetic and cognate data.
"""

import pytest
import csv
import numpy as np
from pathlib import Path

from distfeat import (
    phoneme_to_features,
    calculate_distance,
    build_distance_matrix,
    normalize_ipa
)
from distfeat.alignment import (
    align_sequences,
    align_cognate_set,
    optimize_from_cognates
)


class TestCognateValidation:
    """Test distance metrics against cognate data."""
    
    @pytest.fixture
    def cognate_data(self):
        """Load sample cognate data."""
        data_path = Path(__file__).parent / 'test_data' / 'sample_cognates.csv'
        
        cognates = {}
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cognacy = row['Cognacy']
                    segments = row['Segments'].split()
                    
                    if cognacy not in cognates:
                        cognates[cognacy] = []
                    cognates[cognacy].append(segments)
        
        return list(cognates.values())
    
    def test_cognate_distances(self, cognate_data):
        """Test that cognates have lower distances than non-cognates."""
        if not cognate_data:
            pytest.skip("No cognate data available")
        
        # Calculate intra-cognate distances
        intra_distances = []
        for cognate_set in cognate_data:
            if len(cognate_set) >= 2:
                for i in range(len(cognate_set)):
                    for j in range(i + 1, len(cognate_set)):
                        result = align_sequences(
                            cognate_set[i], cognate_set[j],
                            method='hamming'
                        )
                        intra_distances.append(result.normalized_distance)
        
        # Calculate inter-cognate distances (sample)
        inter_distances = []
        for i in range(min(5, len(cognate_data))):
            for j in range(i + 1, min(5, len(cognate_data))):
                if cognate_data[i] and cognate_data[j]:
                    result = align_sequences(
                        cognate_data[i][0], cognate_data[j][0],
                        method='hamming'
                    )
                    inter_distances.append(result.normalized_distance)
        
        if intra_distances and inter_distances:
            avg_intra = np.mean(intra_distances)
            avg_inter = np.mean(inter_distances)
            
            # Cognates should be closer on average
            assert avg_intra < avg_inter, \
                f"Cognates not closer: intra={avg_intra:.3f}, inter={avg_inter:.3f}"
    
    def test_optimization_from_cognates(self, cognate_data):
        """Test threshold optimization using cognate data."""
        if not cognate_data or len(cognate_data) < 2:
            pytest.skip("Insufficient cognate data")
        
        stats = optimize_from_cognates(cognate_data)
        
        assert 'mean_intra_distance' in stats
        assert 'mean_inter_distance' in stats
        assert 'optimal_threshold' in stats
        
        # Check that statistics make sense
        assert stats['mean_intra_distance'] < stats['mean_inter_distance']
        assert stats['separation'] > 0
        
        # Optimal threshold should be between the means
        assert stats['mean_intra_distance'] < stats['optimal_threshold']
        assert stats['optimal_threshold'] < stats['mean_inter_distance']


class TestIPACharts:
    """Test against known IPA relationships."""
    
    def test_ipa_consonant_chart(self):
        """Test distances match IPA consonant chart structure."""
        # Bilabial stops
        bilabial = ['p', 'b', 'm']
        bilabial_dists = []
        
        for i in range(len(bilabial)):
            for j in range(i + 1, len(bilabial)):
                dist = calculate_distance(bilabial[i], bilabial[j])
                if dist is not None:
                    bilabial_dists.append(dist)
        
        # Alveolar stops
        alveolar = ['t', 'd', 'n']
        alveolar_dists = []
        
        for i in range(len(alveolar)):
            for j in range(i + 1, len(alveolar)):
                dist = calculate_distance(alveolar[i], alveolar[j])
                if dist is not None:
                    alveolar_dists.append(dist)
        
        # Cross-place distances
        cross_dists = []
        for b in bilabial:
            for a in alveolar:
                dist = calculate_distance(b, a)
                if dist is not None:
                    cross_dists.append(dist)
        
        if bilabial_dists and alveolar_dists and cross_dists:
            # Within-place should be closer than across-place
            avg_within = np.mean(bilabial_dists + alveolar_dists)
            avg_cross = np.mean(cross_dists)
            
            assert avg_within < avg_cross, \
                "Place of articulation not properly encoded"
    
    def test_vowel_space(self):
        """Test vowel distances match articulatory space."""
        # Cardinal vowels
        vowels = {
            'i': (1, 0),  # high front
            'e': (0.5, 0),  # mid front
            'a': (0, 0.5),  # low central
            'o': (0.5, 1),  # mid back
            'u': (1, 1),  # high back
        }
        
        # Test that articulatorily close vowels are phonetically close
        dist_ie = calculate_distance('i', 'e')  # Adjacent front
        dist_eo = calculate_distance('e', 'o')  # Front to back
        dist_iu = calculate_distance('i', 'u')  # Opposite corners
        
        if all(d is not None for d in [dist_ie, dist_eo, dist_iu]):
            # Adjacent vowels should be closer than opposite ones
            assert dist_ie < dist_iu, "Vowel height not encoded"
            assert dist_eo < dist_iu, "Vowel space structure incorrect"


class TestSoundChanges:
    """Test known sound change patterns."""
    
    def test_grimms_law(self):
        """Test Germanic sound shift distances."""
        # Grimm's Law correspondences
        shifts = [
            ('p', 'f'),  # p → f
            ('t', 'θ'),  # t → θ (using theta)
            ('k', 'x'),  # k → x/h
            ('b', 'p'),  # b → p
            ('d', 't'),  # d → t
            ('g', 'k'),  # g → k
        ]
        
        distances = []
        for old, new in shifts:
            dist = calculate_distance(old, new)
            if dist is not None:
                distances.append(dist)
        
        if distances:
            avg_shift = np.mean(distances)
            
            # Compare to random pairs
            random_pairs = [('p', 'g'), ('t', 'b'), ('k', 'd')]
            random_dists = []
            for p1, p2 in random_pairs:
                dist = calculate_distance(p1, p2)
                if dist is not None:
                    random_dists.append(dist)
            
            if random_dists:
                avg_random = np.mean(random_dists)
                
                # Sound changes should involve smaller distances
                # than random pairs (though this is a soft constraint)
                assert avg_shift <= avg_random * 1.5, \
                    "Sound change distances unexpectedly large"
    
    def test_palatalization(self):
        """Test palatalization distances."""
        # Common palatalization patterns
        palatalizations = [
            ('k', 'tʃ'),  # k → č before front vowels
            ('g', 'dʒ'),  # g → ǰ
            ('t', 'tʃ'),  # t → č
            ('d', 'dʒ'),  # d → ǰ
        ]
        
        for source, target in palatalizations:
            # Normalize IPA
            source = normalize_ipa(source)
            target = normalize_ipa(target)
            
            dist = calculate_distance(source, target)
            if dist is not None:
                # Palatalization should be a relatively small change
                assert dist < 0.5, \
                    f"Palatalization {source}→{target} distance too large: {dist}"