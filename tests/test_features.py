"""
Unit tests for phonetic feature extraction.
"""

import pytest
from distfeat import (
    phoneme_to_features, 
    features_to_phoneme,
    get_feature_system,
    get_feature_names,
    load_custom_features
)


class TestPhonemeToFeatures:
    """Test phoneme to feature conversion."""
    
    def test_basic_phonemes(self):
        """Test common phonemes have expected features."""
        # Voiceless bilabial stop
        p_features = phoneme_to_features('p')
        assert p_features is not None
        assert isinstance(p_features, dict)
        
        # Voiced bilabial stop
        b_features = phoneme_to_features('b')
        assert b_features is not None
        
        # Vowels
        a_features = phoneme_to_features('a')
        assert a_features is not None
        
        i_features = phoneme_to_features('i')
        assert i_features is not None
    
    def test_missing_phoneme(self):
        """Test handling of unknown phonemes."""
        # With default error handling (warn)
        result = phoneme_to_features('zzz')
        assert result is None
        
        # With raise error handling
        with pytest.raises(ValueError):
            phoneme_to_features('zzz', on_error='raise')
        
        # With ignore error handling
        result = phoneme_to_features('zzz', on_error='ignore')
        assert result is None
    
    def test_feature_consistency(self):
        """Test that feature vectors have consistent length."""
        p_features = phoneme_to_features('p')
        b_features = phoneme_to_features('b')
        
        assert len(p_features) == len(b_features)
        assert set(p_features.keys()) == set(b_features.keys())


class TestFeaturesToPhoneme:
    """Test feature to phoneme conversion."""
    
    def test_exact_match(self):
        """Test exact feature matching."""
        # Get features for 'p'
        p_features = phoneme_to_features('p')
        
        # Should recover some phoneme with identical features
        result = features_to_phoneme(p_features)
        assert result is not None
        
        # The recovered phoneme should have the same features as 'p'
        result_features = phoneme_to_features(result)
        assert p_features == result_features
    
    def test_partial_match(self):
        """Test partial feature matching."""
        # Create partial feature set
        partial = {'voice': 0, 'labial': 1}
        
        # Should find best match
        result = features_to_phoneme(partial, threshold=0.5)
        assert result is not None
    
    def test_no_match(self):
        """Test when no phoneme matches."""
        # Create impossible feature combination
        impossible = {'voice': 2, 'labial': 3}
        
        result = features_to_phoneme(impossible)
        assert result is None


class TestFeatureSystem:
    """Test feature system access."""
    
    def test_get_feature_system(self):
        """Test retrieving complete feature system."""
        system = get_feature_system()
        
        assert isinstance(system, dict)
        assert len(system) > 0
        
        # Check structure
        for phoneme, data in system.items():
            assert 'features' in data
            assert isinstance(data['features'], dict)
    
    def test_get_feature_names(self):
        """Test retrieving feature names."""
        names = get_feature_names()
        
        assert isinstance(names, list)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)
    
    def test_filter_phonemes(self):
        """Test filtering phonemes by type."""
        # Get all phonemes
        all_system = get_feature_system()
        
        # Filter clicks
        no_clicks = get_feature_system(exclude_clicks=True)
        
        # Should have fewer phonemes
        assert len(no_clicks) <= len(all_system)
    
    def test_matrix_conversion(self):
        """Test converting to matrix format."""
        import numpy as np
        
        matrix = get_feature_system(as_matrix=True)
        
        assert isinstance(matrix, np.ndarray)
        assert len(matrix.shape) == 2
        assert matrix.shape[0] > 0  # Number of phonemes
        assert matrix.shape[1] > 0  # Number of features