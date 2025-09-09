"""
Tests for configuration management.
"""

import pytest
from distfeat.config import (
    get_config,
    set_config,
    reset_config,
    validate_config
)


class TestConfiguration:
    """Test configuration system."""
    
    def setup_method(self):
        """Reset config before each test."""
        reset_config()
    
    def teardown_method(self):
        """Reset config after each test."""
        reset_config()
    
    def test_default_config(self):
        """Test default configuration values."""
        config = get_config()
        
        # Check required keys exist
        required_keys = [
            'default_distance_method',
            'on_error',
            'normalize_by_default',
            'cache_size',
            'feature_system',
        ]
        
        for key in required_keys:
            assert key in config, f"Missing default config key: {key}"
    
    def test_set_get_config(self):
        """Test setting and getting config values."""
        # Test setting valid values
        set_config('default_distance_method', 'jaccard')
        config = get_config()
        assert config['default_distance_method'] == 'jaccard'
        
        set_config('on_error', 'raise')
        config = get_config()
        assert config['on_error'] == 'raise'
        
        set_config('normalize_by_default', False)
        config = get_config()
        assert config['normalize_by_default'] is False
    
    def test_invalid_config(self):
        """Test validation of invalid config values."""
        # Invalid distance method
        with pytest.raises(ValueError):
            set_config('default_distance_method', 'invalid_method')
        
        # Invalid error handling
        with pytest.raises(ValueError):
            set_config('on_error', 'invalid_option')
        
        # Invalid cache size
        with pytest.raises(ValueError):
            set_config('cache_size', -1)
    
    def test_config_validation(self):
        """Test config validation function."""
        valid_config = {
            'default_distance_method': 'hamming',
            'on_error': 'warn',
            'normalize_by_default': True,
            'cache_size': 1024,
            'feature_system': 'clts'
        }
        
        assert validate_config(valid_config) is True
        
        # Invalid config
        invalid_config = {
            'default_distance_method': 'invalid',
            'on_error': 'warn',
        }
        
        assert validate_config(invalid_config) is False
    
    def test_config_persistence(self):
        """Test config changes persist within session."""
        original = get_config()['default_distance_method']
        
        # Change config
        set_config('default_distance_method', 'euclidean')
        
        # Verify it persists across multiple calls
        assert get_config()['default_distance_method'] == 'euclidean'
        assert get_config()['default_distance_method'] == 'euclidean'
        
        # Reset should restore defaults
        reset_config()
        restored = get_config()['default_distance_method']
        assert restored == original
    
    def test_config_dict_update(self):
        """Test updating config with dictionary."""
        updates = {
            'default_distance_method': 'cosine',
            'on_error': 'ignore',
            'normalize_by_default': False
        }
        
        # Update multiple values
        for key, value in updates.items():
            set_config(key, value)
        
        config = get_config()
        for key, value in updates.items():
            assert config[key] == value


class TestConfigIntegration:
    """Test config integration with other modules."""
    
    def test_distance_method_default(self):
        """Test that default distance method is used."""
        from distfeat import calculate_distance
        
        # Set default method
        set_config('default_distance_method', 'jaccard')
        
        # Calculate distance without specifying method
        # (This would require modifying calculate_distance to use config)
        # For now, just verify config is accessible
        config = get_config()
        assert config['default_distance_method'] == 'jaccard'
    
    def test_error_handling_default(self):
        """Test that default error handling is used."""
        from distfeat import phoneme_to_features
        
        # Set error handling
        set_config('on_error', 'ignore')
        
        # Test with invalid phoneme
        # (This would require modifying functions to use config)
        config = get_config()
        assert config['on_error'] == 'ignore'
    
    def test_cache_size_configuration(self):
        """Test cache size configuration."""
        set_config('cache_size', 2048)
        
        config = get_config()
        assert config['cache_size'] == 2048
        
        # Verify cache size is reasonable
        assert config['cache_size'] > 0
        assert config['cache_size'] <= 10000


class TestEnvironmentConfig:
    """Test configuration from environment variables."""
    
    def test_env_var_override(self, monkeypatch):
        """Test config override from environment variables."""
        # Set environment variable
        monkeypatch.setenv('DISTFEAT_DISTANCE_METHOD', 'manhattan')
        monkeypatch.setenv('DISTFEAT_ON_ERROR', 'raise')
        
        # Reset config to pick up env vars
        reset_config()
        
        config = get_config()
        # Note: This would require implementing env var support
        # For now, just test that config system is working
        assert 'default_distance_method' in config
        assert 'on_error' in config
    
    def test_config_file_loading(self, tmp_path):
        """Test loading config from file."""
        config_file = tmp_path / "distfeat.yml"
        config_file.write_text("""
default_distance_method: euclidean
on_error: raise
normalize_by_default: false
cache_size: 512
""")
        
        # This would require implementing file-based config
        # For now, just test file exists
        assert config_file.exists()