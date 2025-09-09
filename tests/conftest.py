"""
Pytest configuration and fixtures for distfeat tests.
"""

import pytest
import numpy as np
import tempfile
import shutil
from pathlib import Path

# Test data and fixtures

@pytest.fixture(scope="session")
def test_phonemes():
    """Standard set of test phonemes for consistent testing."""
    return {
        'consonants': ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 'v', 's', 'z'],
        'vowels': ['i', 'e', 'a', 'o', 'u', 'ɪ', 'ʊ', 'ə'],
        'stops': ['p', 'b', 't', 'd', 'k', 'g'],
        'fricatives': ['f', 'v', 's', 'z', 'ʃ', 'ʒ', 'x', 'ɣ'],
        'nasals': ['m', 'n', 'ŋ', 'ɲ'],
        'liquids': ['l', 'r', 'ɾ', 'ɭ'],
    }

@pytest.fixture(scope="session")
def sample_distance_matrix():
    """Sample distance matrix for testing I/O operations."""
    phonemes = ['p', 'b', 't', 'd']
    matrix = np.array([
        [0.0, 0.1, 0.3, 0.4],
        [0.1, 0.0, 0.4, 0.3],
        [0.3, 0.4, 0.0, 0.1],
        [0.4, 0.3, 0.1, 0.0]
    ])
    return matrix, phonemes

@pytest.fixture
def temp_dir():
    """Temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_cognate_data():
    """Sample cognate data for testing alignment and validation."""
    return {
        'cognate_set_1': [
            ['d', 'o', 'g'],    # English
            ['h', 'u', 'n', 't'],  # German Hund
        ],
        'cognate_set_2': [
            ['k', 'a', 't'],   # English cat
            ['k', 'a', 't', 's', 'ə'],  # German Katze
        ],
        'cognate_set_3': [
            ['w', 'a', 't', 'ə', 'r'],  # English water
            ['v', 'a', 's', 'ə', 'r'],  # German Wasser
        ]
    }

@pytest.fixture
def feature_test_cases():
    """Test cases for feature extraction."""
    return {
        'basic': {
            'p': {'voice': 0, 'labial': 1, 'consonantal': 1},
            'b': {'voice': 1, 'labial': 1, 'consonantal': 1},
            'a': {'voice': 1, 'low': 1, 'consonantal': 0},
        },
        'complex': {
            'pʰ': {'voice': 0, 'labial': 1, 'aspirated': 1},
            'tʃ': {'voice': 0, 'coronal': 1, 'delayed_release': 1},
            'ã': {'voice': 1, 'low': 1, 'nasal': 1},
        }
    }

# Pytest markers for organizing tests

def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance benchmarks"
    )
    config.addinivalue_line(
        "markers", "linguistic: marks tests that validate linguistic properties"
    )

# Test utilities

def assert_matrix_properties(matrix, labels):
    """Assert basic properties of distance matrices."""
    n = len(labels)
    assert matrix.shape == (n, n), f"Matrix shape {matrix.shape} != ({n}, {n})"
    assert np.allclose(matrix, matrix.T), "Matrix not symmetric"
    assert np.allclose(np.diag(matrix), 0), "Diagonal not zero"
    assert np.all(matrix >= 0), "Negative distances found"
    assert np.all(np.isfinite(matrix)), "Non-finite values in matrix"

def assert_distance_properties(distance):
    """Assert basic properties of distance values."""
    assert isinstance(distance, (int, float)), f"Distance not numeric: {type(distance)}"
    assert distance >= 0, f"Negative distance: {distance}"
    assert np.isfinite(distance), f"Non-finite distance: {distance}"

def fuzzy_equal(a, b, tolerance=1e-6):
    """Check if two values are approximately equal."""
    return abs(a - b) < tolerance

# Skip conditions

skip_if_no_sklearn = pytest.mark.skipif(
    not _has_sklearn(), reason="scikit-learn not available"
)

skip_if_no_memory_profiler = pytest.mark.skipif(
    not _has_memory_profiler(), reason="memory_profiler not available"
)

def _has_sklearn():
    """Check if sklearn is available."""
    try:
        import sklearn
        return True
    except ImportError:
        return False

def _has_memory_profiler():
    """Check if memory_profiler is available."""
    try:
        import memory_profiler
        return True
    except ImportError:
        return False

# Test data generators

def generate_phoneme_pairs(phonemes, max_pairs=100):
    """Generate phoneme pairs for testing."""
    pairs = []
    for i, p1 in enumerate(phonemes):
        for j, p2 in enumerate(phonemes[i:], i):
            if len(pairs) >= max_pairs:
                break
            pairs.append((p1, p2))
        if len(pairs) >= max_pairs:
            break
    return pairs

def generate_test_matrix(size, seed=42):
    """Generate a test distance matrix with known properties."""
    np.random.seed(seed)
    # Generate random symmetric matrix
    matrix = np.random.rand(size, size)
    matrix = (matrix + matrix.T) / 2
    np.fill_diagonal(matrix, 0)
    return matrix

# Performance testing utilities

class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, description="Operation"):
        self.description = description
        self.start_time = None
        self.elapsed_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_time = time.time() - self.start_time
        print(f"{self.description}: {self.elapsed_time:.4f}s")

# Memory testing utilities (requires memory_profiler)

def memory_usage_mb():
    """Get current memory usage in MB."""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        return None

class MemoryMonitor:
    """Monitor memory usage during operations."""
    
    def __init__(self, description="Operation"):
        self.description = description
        self.initial_memory = None
        self.peak_memory = None
        self.final_memory = None
    
    def __enter__(self):
        self.initial_memory = memory_usage_mb()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.final_memory = memory_usage_mb()
        if self.initial_memory and self.final_memory:
            memory_increase = self.final_memory - self.initial_memory
            print(f"{self.description}: {memory_increase:+.2f} MB memory change")

# Test validation utilities

def validate_linguistic_distance(phoneme1, phoneme2, distance, expected_range=None):
    """Validate that a distance makes linguistic sense."""
    assert_distance_properties(distance)
    
    if expected_range:
        min_dist, max_dist = expected_range
        assert min_dist <= distance <= max_dist, \
            f"Distance {phoneme1}-{phoneme2} ({distance:.3f}) outside expected range [{min_dist}, {max_dist}]"

def validate_cognate_alignment(alignment_result, max_distance=1.0):
    """Validate cognate alignment results."""
    assert hasattr(alignment_result, 'distance'), "Missing distance attribute"
    assert hasattr(alignment_result, 'seq1_aligned'), "Missing seq1_aligned attribute"
    assert hasattr(alignment_result, 'seq2_aligned'), "Missing seq2_aligned attribute"
    
    assert_distance_properties(alignment_result.distance)
    assert alignment_result.distance <= max_distance, \
        f"Cognate distance too high: {alignment_result.distance}"
    
    # Aligned sequences should have same length
    assert len(alignment_result.seq1_aligned) == len(alignment_result.seq2_aligned), \
        "Aligned sequences have different lengths"