# distfeat

**Distance and Feature library for phonetic analysis**

A focused Python library for phonetic feature extraction and distance calculation, with comprehensive IPA support and glyph normalization.

## Features

- 🎯 **Phonetic Features**: Binary feature vectors for 1000+ IPA phonemes from CLTS BIPA
- 📏 **Distance Metrics**: Multiple methods including Hamming, Jaccard, Euclidean, Cosine, Manhattan, and K-means clustering
- 🔤 **IPA Normalization**: Comprehensive glyph normalization with NFD, diacritic ordering, and IPA canonicalization
- 🧪 **Cognate Testing**: Built-in alignment and optimization tools for historical linguistics
- ⚡ **Fast & Lightweight**: Minimal dependencies, optimized caching, pure Python with NumPy acceleration
- 🔧 **Extensible**: Register custom distance methods and feature systems

## Installation

```bash
pip install distfeat
```

For development:
```bash
pip install distfeat[dev]
```

## Quick Start

### Basic Usage

```python
from distfeat import phoneme_to_features, calculate_distance

# Get phonetic features
features_p = phoneme_to_features('p')
features_b = phoneme_to_features('b')

# Calculate distance between phonemes
distance = calculate_distance('p', 'b', method='hamming')
print(f"Distance between 'p' and 'b': {distance:.3f}")
# Output: Distance between 'p' and 'b': 0.053
```

### Build Distance Matrix

```python
from distfeat import build_distance_matrix

# Build matrix for specific phonemes
phonemes = ['p', 'b', 't', 'd', 'k', 'g']
matrix, labels = build_distance_matrix(phonemes, method='hamming')

# Or build for all phonemes in the system
matrix, labels = build_distance_matrix(method='jaccard')
```

### IPA Normalization

```python
from distfeat import normalize_ipa, normalize_glyph

# Normalize IPA text
text = "pʰæ̃n"
normalized = normalize_ipa(text)
print(normalized)  # "pʰæ̃n" with consistent encoding

# Fine-grained control
normalized = normalize_glyph(
    text,
    nfd=True,
    order_diacritics=True,
    normalize_length=True,
    preserve_tones=False
)
```

### Export Distance Matrices

```python
from distfeat import save_distance_matrix, load_distance_matrix

# Save in different formats
save_distance_matrix(matrix, phonemes, 'distances.tsv', format='tsv')
save_distance_matrix(matrix, phonemes, 'distances.json', format='json')

# Load matrices
loaded_matrix, loaded_phonemes = load_distance_matrix('distances.tsv')
```

## Distance Methods

### Built-in Methods

- **Hamming**: Number of differing features (normalized)
- **Jaccard**: 1 - (intersection/union) of active features
- **Euclidean**: L2 distance in feature space
- **Cosine**: 1 - cosine similarity
- **Manhattan**: L1 distance (sum of absolute differences)
- **K-means**: Clustering-based distance using centroids

### Custom Distance Methods

```python
from distfeat import register_distance_method, calculate_distance
import numpy as np

# Define custom distance
def weighted_hamming(vec1, vec2):
    weights = np.linspace(1, 2, len(vec1))  # Weight later features more
    return np.sum(weights * (vec1 != vec2)) / np.sum(weights)

# Register and use
register_distance_method('weighted_hamming', weighted_hamming)
distance = calculate_distance('p', 'b', method='weighted_hamming')
```

## Configuration

### Programmatic Configuration

```python
from distfeat import get_config, set_config

# Get current configuration
config = get_config()

# Modify settings
set_config('default_distance_method', 'jaccard')
set_config('on_error', 'raise')  # 'raise', 'warn', or 'ignore'
set_config('kmeans_clusters', 15)
```

### YAML Configuration

```yaml
# config.yaml
default_distance_method: hamming
default_normalize: true
default_precision: 4
cache_size: 2048
kmeans_clusters: 12
on_error: warn
```

```python
from distfeat import load_config

load_config('config.yaml')
```

## Custom Feature Systems

```python
from distfeat import load_custom_features, phoneme_to_features

# Load custom feature system
load_custom_features(
    'my_features.csv',
    name='custom',
    delimiter=',',
    phoneme_col='IPA'
)

# Use custom system
features = phoneme_to_features('p', system='custom')
```

## Testing & Validation

The library includes comprehensive tests for:

- **Unit Tests**: Core functionality for features and distances
- **Property Tests**: Mathematical properties (symmetry, triangle inequality)
- **Linguistic Tests**: Voice distinctions, place of articulation, manner classes
- **Integration Tests**: Validation against cognate data and IPA charts

Run tests:
```bash
pytest tests/
```

## Data Sources

- **CLTS BIPA**: Phonetic features from the Cross-Linguistic Transcription Systems project
- **Bundled Data**: Complete feature system for 1000+ IPA phonemes included
- **Test Data**: Sample cognate sets for validation (not included in distribution)

## API Reference

### Core Functions

- `phoneme_to_features(phoneme, system=None, on_error='warn')`: Convert phoneme to features
- `features_to_phoneme(features, system=None, threshold=1.0)`: Find best matching phoneme
- `calculate_distance(phoneme1, phoneme2, method='hamming', normalize=True)`: Calculate distance
- `build_distance_matrix(phonemes=None, method='hamming')`: Build distance matrix

### Normalization

- `normalize_ipa(text, canonicalize=True, decompose_affricates=False)`: Normalize IPA text
- `normalize_glyph(text, nfd=True, order_diacritics=True, ...)`: Fine-grained normalization

### I/O Functions

- `save_distance_matrix(matrix, phonemes, path, format='tsv')`: Save matrix
- `load_distance_matrix(path, format=None)`: Load matrix
- `export_matrix_tsv/csv/json(...)`: Format-specific exports

## Performance

- **Caching**: LRU cache for distance calculations (configurable size)
- **Vectorization**: NumPy arrays for efficient computation
- **Lazy Loading**: Features loaded on first use

## Contributing

Contributions welcome! The library is designed to be extended with:
- New distance methods
- Additional feature systems
- Enhanced normalization rules
- Performance optimizations

## License

MIT License - see LICENSE file for details.

## Citation

If you use distfeat in your research, please cite:

```bibtex
@software{distfeat,
  title = {distfeat: Distance and Feature library for phonetic analysis},
  author = {UNIPA Development Team},
  year = {2024},
  url = {https://github.com/your-org/distfeat}
}
```

## Related Projects

- [UNIPA](https://github.com/your-org/unipa): Parent project for computational historical linguistics
- [CLTS](https://clts.clld.org/): Cross-Linguistic Transcription Systems
- [LingPy](https://lingpy.org/): Python library for historical linguistics