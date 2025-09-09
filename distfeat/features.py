"""
Phonetic feature extraction and manipulation.

Core functionality for converting between phonemes and feature vectors.
"""

import csv
import importlib.resources as resources
import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

logger = logging.getLogger('distfeat')

# Global feature system cache
_FEATURE_CACHE: Optional[Dict[str, Dict]] = None
_FEATURE_NAMES: Optional[List[str]] = None
_CUSTOM_SYSTEMS: Dict[str, Dict] = {}


def _load_bundled_features() -> Tuple[Dict[str, Dict], List[str]]:
    """Load the bundled feature system from feature_system.csv."""
    try:
        # Try loading feature_system.csv first (our proper format)
        data_path = Path(__file__).parent / 'data' / 'feature_system.csv'
        if data_path.exists():
            return _load_csv_features(data_path)
        
        # Fallback to package resources
        data = resources.read_text('distfeat.data', 'feature_system.csv')
        lines = data.strip().split('\n')
        return _parse_csv_lines(lines)
        
    except Exception:
        # Final fallback - try graphemes.tsv (original CLTS format)
        data_path = Path(__file__).parent / 'data' / 'graphemes.tsv'
        if data_path.exists():
            return _load_clts_fallback(data_path)
        
        raise FileNotFoundError(
            "Feature system data not found. Please ensure feature_system.csv "
            "is in the distfeat/data directory."
        )

def _load_csv_features(csv_path: Path) -> Tuple[Dict[str, Dict], List[str]]:
    """Load features from CSV file."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return _parse_csv_lines([line.strip() for line in lines])

def _parse_csv_lines(lines: List[str]) -> Tuple[Dict[str, Dict], List[str]]:
    """Parse CSV lines into feature data."""
    features = {}
    feature_names = []
    
    reader = csv.DictReader(lines)
    
    for row in reader:
        if not feature_names:
            # Extract feature columns (exclude metadata)
            exclude_cols = {'sound', 'description', 'phoneme', 'name', 'IPA'}
            feature_names = [col for col in row.keys() if col not in exclude_cols]
        
        phoneme = row.get('sound') or row.get('phoneme') or row.get('IPA')
        if not phoneme:
            continue
            
        # Extract feature values - handle -1, 0, 1 format
        feature_vec = {}
        for fname in feature_names:
            val = row.get(fname, '0')
            try:
                # Convert to int, then to binary (negative = 0, positive = 1)
                numeric_val = int(float(val)) if val not in ['', 'n/a'] else 0
                feature_vec[fname] = 1 if numeric_val > 0 else 0
            except (ValueError, TypeError):
                feature_vec[fname] = 0
        
        features[phoneme] = {
            'features': feature_vec,
            'name': row.get('description', row.get('name', '')),
            'generated': False
        }
    
    return features, feature_names

def _load_clts_fallback(tsv_path: Path) -> Tuple[Dict[str, Dict], List[str]]:
    """Fallback loader for original CLTS graphemes.tsv format."""
    # This is a minimal implementation for the raw CLTS data
    # In practice, we need the processed feature system
    raise NotImplementedError(
        "Raw CLTS data loading not implemented. "
        "Please use a processed feature_system.csv file."
    )


def _initialize_features() -> None:
    """Initialize the global feature cache."""
    global _FEATURE_CACHE, _FEATURE_NAMES
    if _FEATURE_CACHE is None:
        _FEATURE_CACHE, _FEATURE_NAMES = _load_bundled_features()
        logger.info(f"Loaded {len(_FEATURE_CACHE)} phonemes with {len(_FEATURE_NAMES)} features")


@lru_cache(maxsize=1024)
def phoneme_to_features(
    phoneme: str, 
    system: Optional[str] = None,
    on_error: str = 'warn'
) -> Optional[Dict[str, int]]:
    """
    Convert a phoneme to its feature dictionary.
    
    Args:
        phoneme: IPA phoneme string
        system: Feature system to use (None for default CLTS)
        on_error: Error handling - 'raise', 'warn', or 'ignore'
        
    Returns:
        Dictionary of feature names to values (0 or 1), or None if not found
        
    Raises:
        ValueError: If phoneme not found and on_error='raise'
    """
    _initialize_features()
    
    # Select feature system
    if system is None:
        feature_data = _FEATURE_CACHE
    elif system in _CUSTOM_SYSTEMS:
        feature_data = _CUSTOM_SYSTEMS[system]
    else:
        raise ValueError(f"Unknown feature system: {system}")
    
    # Look up phoneme
    if phoneme in feature_data:
        return feature_data[phoneme]['features'].copy()
    
    # Handle missing phoneme
    if on_error == 'raise':
        raise ValueError(f"Phoneme '{phoneme}' not found in feature system")
    elif on_error == 'warn':
        logger.warning(f"Phoneme '{phoneme}' not found in feature system")
    
    return None


def features_to_phoneme(
    features: Dict[str, int],
    system: Optional[str] = None,
    threshold: float = 1.0
) -> Optional[str]:
    """
    Find the phoneme that best matches the given features.
    
    Args:
        features: Dictionary of feature names to values
        system: Feature system to use
        threshold: Minimum similarity threshold (0.0 to 1.0)
        
    Returns:
        Best matching phoneme, or None if no match above threshold
    """
    _initialize_features()
    
    # Select feature system
    if system is None:
        feature_data = _FEATURE_CACHE
    else:
        feature_data = _CUSTOM_SYSTEMS[system]
    
    best_match = None
    best_score = 0.0
    
    for phoneme, data in feature_data.items():
        phoneme_features = data['features']
        
        # Calculate exact match score (all features must match)
        all_features = set(features.keys()) | set(phoneme_features.keys())
        if not all_features:
            continue
            
        matches = sum(1 for f in all_features 
                     if features.get(f, 0) == phoneme_features.get(f, 0))
        score = matches / len(all_features)
        
        if score > best_score:
            best_score = score
            best_match = phoneme
    
    return best_match if best_score >= threshold else None


def get_feature_system(
    system: Optional[str] = None,
    as_matrix: bool = False,
    exclude_clicks: bool = False,
    exclude_tones: bool = False,
    exclude_diacritics: bool = False
) -> Union[Dict[str, Dict], np.ndarray]:
    """
    Get the complete feature system.
    
    Args:
        system: Feature system name (None for default)
        as_matrix: Return as numpy matrix instead of dictionary
        exclude_clicks: Filter out click consonants
        exclude_tones: Filter out tonal features
        exclude_diacritics: Filter out diacritical marks
        
    Returns:
        Dictionary mapping phonemes to feature data, or numpy matrix
    """
    _initialize_features()
    
    if system is None:
        feature_data = _FEATURE_CACHE.copy()
    else:
        feature_data = _CUSTOM_SYSTEMS[system].copy()
    
    # Apply filters
    if exclude_clicks:
        feature_data = {k: v for k, v in feature_data.items() 
                       if not _is_click(k)}
    
    if exclude_tones:
        feature_data = {k: v for k, v in feature_data.items()
                       if not _has_tone(k)}
    
    if exclude_diacritics:
        feature_data = {k: v for k, v in feature_data.items()
                       if not _has_diacritic(k)}
    
    if as_matrix:
        # Convert to numpy matrix
        phonemes = sorted(feature_data.keys())
        feature_names = get_feature_names(system)
        
        matrix = np.zeros((len(phonemes), len(feature_names)))
        for i, phoneme in enumerate(phonemes):
            features = feature_data[phoneme]['features']
            for j, fname in enumerate(feature_names):
                matrix[i, j] = features.get(fname, 0)
        
        return matrix
    
    return feature_data


def get_feature_names(system: Optional[str] = None) -> List[str]:
    """
    Get the list of feature names in order.
    
    Args:
        system: Feature system name
        
    Returns:
        List of feature names
    """
    _initialize_features()
    
    if system is None:
        return _FEATURE_NAMES.copy()
    elif system in _CUSTOM_SYSTEMS:
        # Get feature names from first phoneme
        first_phoneme = next(iter(_CUSTOM_SYSTEMS[system].values()))
        return list(first_phoneme['features'].keys())
    else:
        raise ValueError(f"Unknown feature system: {system}")


def load_custom_features(
    path: Union[str, Path],
    name: str,
    delimiter: str = '\t',
    phoneme_col: str = 'phoneme',
    exclude_cols: Optional[List[str]] = None
) -> None:
    """
    Load a custom feature system from a file.
    
    Args:
        path: Path to feature file (CSV or TSV)
        name: Name to register the system under
        delimiter: Column delimiter
        phoneme_col: Name of the phoneme column
        exclude_cols: Columns to exclude from features
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {path}")
    
    if exclude_cols is None:
        exclude_cols = [phoneme_col, 'description', 'name', 'note']
    
    features = {}
    feature_names = []
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        
        for row in reader:
            if not feature_names:
                feature_names = [col for col in row.keys() 
                               if col not in exclude_cols]
            
            phoneme = row[phoneme_col]
            feature_vec = {}
            
            for fname in feature_names:
                val = row.get(fname, '0')
                # Convert to binary
                if val in ['', 'n', '0', '-']:
                    feature_vec[fname] = 0
                else:
                    try:
                        feature_vec[fname] = int(float(val))
                    except (ValueError, TypeError):
                        feature_vec[fname] = 1
            
            features[phoneme] = {
                'features': feature_vec,
                'name': row.get('name', ''),
                'custom': True
            }
    
    _CUSTOM_SYSTEMS[name] = features
    logger.info(f"Loaded custom feature system '{name}' with {len(features)} phonemes")


def _is_click(phoneme: str) -> bool:
    """Check if phoneme is a click consonant."""
    click_chars = set('ǀǁǂǃʘ')
    return any(c in click_chars for c in phoneme)


def _has_tone(phoneme: str) -> bool:
    """Check if phoneme has tone markers."""
    # Unicode tone marks and tone numbers
    import unicodedata
    for char in phoneme:
        if unicodedata.category(char) in ('Mn', 'Sk'):
            name = unicodedata.name(char, '')
            if 'TONE' in name:
                return True
    # Also check for numbered tones
    return any(c in '¹²³⁴⁵₁₂₃₄₅' for c in phoneme)


def _has_diacritic(phoneme: str) -> bool:
    """Check if phoneme has diacritical marks."""
    import unicodedata
    for char in phoneme:
        if unicodedata.category(char) == 'Mn':
            return True
    return False