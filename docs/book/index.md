# distfeat: A Phonetic Distance and Feature Library for Computational Historical Linguistics

```{admonition} Abstract
:class: abstract

We present **distfeat**, a Python library for phonetic feature extraction and distance calculation designed specifically for computational historical linguistics. The library provides a unified framework for converting International Phonetic Alphabet (IPA) symbols to binary feature vectors, calculating phonetic distances using multiple metrics, and validating these distances against cognate data. Our implementation includes comprehensive IPA normalization, six distance metrics (Hamming, Jaccard, Euclidean, Cosine, Manhattan, and K-means clustering), and built-in optimization using aligned cognate sets. We validate our approach across six language families, demonstrating that phonetic distances correlate strongly with cognate relationships. The library's simple functional API, minimal dependencies, and extensive test coverage make it suitable for both research and production use. distfeat is released as open-source software to facilitate reproducible research in computational historical linguistics.
```

## Overview

**distfeat** addresses a fundamental challenge in computational historical linguistics: quantifying phonetic similarity between sounds across languages. While linguists have long understood that certain sounds are more similar than others (e.g., [p] and [b] differ only in voicing), computational methods require precise, reproducible metrics.

This library provides:
- 🎯 **Phonetic Features**: Binary feature vectors for 1000+ IPA phonemes from CLTS BIPA
- 📏 **Distance Metrics**: Multiple validated methods for measuring phonetic similarity
- 🔤 **IPA Normalization**: Robust handling of diacritics, tone marks, and encoding variants
- 🧪 **Cognate Validation**: Built-in tools for optimizing distances using aligned cognate sets
- ⚡ **Performance**: Optimized implementation with caching and vectorization
- 🔧 **Extensibility**: Support for custom feature systems and distance methods

## Key Features

### Unified Framework
Unlike existing tools that focus on specific aspects, distfeat provides an integrated solution:
- Feature extraction from IPA symbols
- Multiple distance calculation methods
- Validation against real linguistic data
- Optimization using cognate sets

### Theoretical Grounding
Our approach is based on:
- Articulatory phonetics (place, manner, voicing)
- Acoustic phonetics (formant structures)
- Historical linguistics (sound change patterns)
- Information theory (feature importance)

### Practical Design
- **Simple API**: Functional interface with sensible defaults
- **Minimal Dependencies**: Only NumPy and scikit-learn required
- **Comprehensive Testing**: Unit, property, and integration tests
- **Documentation**: Full API reference with examples

## Installation

```bash
pip install distfeat
```

For development:
```bash
pip install distfeat[dev]
```

## Quick Example

```python
from distfeat import phoneme_to_features, calculate_distance, build_distance_matrix

# Get phonetic features for a sound
features_p = phoneme_to_features('p')
print(f"Features for [p]: {list(features_p.items())[:5]}...")
# Features for [p]: [('consonantal', 1), ('sonorant', 0), ('syllabic', 0), ('labial', 1), ('coronal', 0)]...

# Calculate distance between two sounds
distance = calculate_distance('p', 'b', method='hamming')
print(f"Distance between [p] and [b]: {distance:.3f}")
# Distance between [p] and [b]: 0.053

# Build a distance matrix for multiple sounds
phonemes = ['p', 'b', 't', 'd', 'k', 'g']
matrix, labels = build_distance_matrix(phonemes, method='hamming')
print(f"Matrix shape: {matrix.shape}")
# Matrix shape: (6, 6)
```

## Citation

If you use distfeat in your research, please cite:

```bibtex
@software{distfeat2024,
  title = {distfeat: A Phonetic Distance and Feature Library for Computational Historical Linguistics},
  author = {UNIPA Development Team},
  year = {2024},
  url = {https://github.com/your-org/distfeat},
  version = {0.1.0}
}
```

## Navigation

```{tableofcontents}
```

## Contact

- **GitHub**: [github.com/your-org/distfeat](https://github.com/your-org/distfeat)
- **PyPI**: [pypi.org/project/distfeat](https://pypi.org/project/distfeat)
- **Issues**: [github.com/your-org/distfeat/issues](https://github.com/your-org/distfeat/issues)

## License

distfeat is released under the MIT License. See [LICENSE](https://github.com/your-org/distfeat/blob/main/LICENSE) for details.