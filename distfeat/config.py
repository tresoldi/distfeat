"""
Configuration management for distfeat.

Supports both programmatic and YAML-based configuration.
"""

import logging
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger('distfeat')

# Global configuration dictionary
_CONFIG: Dict[str, Any] = {
    # Default configuration values
    'default_distance_method': 'hamming',
    'default_normalize': True,
    'default_precision': 4,
    'cache_size': 1024,
    'kmeans_clusters': 12,
    'on_error': 'warn',  # 'raise', 'warn', 'ignore'
    'logging_level': 'INFO',
}


def get_config(key: Optional[str] = None) -> Any:
    """
    Get configuration value(s).
    
    Args:
        key: Configuration key (None to get all config)
        
    Returns:
        Configuration value or full config dict
    """
    if key is None:
        return _CONFIG.copy()
    
    return _CONFIG.get(key)


def set_config(key: str, value: Any) -> None:
    """
    Set configuration value.
    
    Args:
        key: Configuration key
        value: Configuration value
    """
    _CONFIG[key] = value
    logger.debug(f"Config set: {key} = {value}")


def load_config(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        path: Path to YAML configuration file
        
    Returns:
        Loaded configuration dictionary
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Update global config
    _CONFIG.update(config)
    
    # Apply logging level if specified
    if 'logging_level' in config:
        logging.getLogger('distfeat').setLevel(config['logging_level'])
    
    logger.info(f"Loaded configuration from {path}")
    
    return config


def save_config(path: Union[str, Path]) -> None:
    """
    Save current configuration to YAML file.
    
    Args:
        path: Output path for YAML file
    """
    path = Path(path)
    
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(_CONFIG, f, default_flow_style=False)
    
    logger.info(f"Saved configuration to {path}")


def reset_config() -> None:
    """Reset configuration to defaults."""
    global _CONFIG
    _CONFIG = {
        'default_distance_method': 'hamming',
        'default_normalize': True,
        'default_precision': 4,
        'cache_size': 1024,
        'kmeans_clusters': 12,
        'on_error': 'warn',
        'logging_level': 'INFO',
    }
    logger.info("Configuration reset to defaults")