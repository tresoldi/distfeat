# distfeat

Standalone phonological feature systems for `alteruphono` and other Python
libraries.

`distfeat` is the canonical home for:

- phonological feature datasets
- feature system protocols and registries
- feature geometry and distance logic
- built-in systems: `ipa`, `tresoldi`, `distinctive`

The package is currently developed inside the `alteruphono` repository, but it
is structured as a standalone subproject so it can be split into its own
repository cleanly.

## Main Concepts

### Dataset

A `FeatureDataset` is the source of truth for feature data. It contains:

- `sounds`: grapheme to descriptive name
- `classes`: sound class definitions and class feature strings
- `features`: `(value, feature)` pairs

The built-in package dataset is bundled as TSV files, and users can also load
their own datasets.

### System

A feature system implements the `FeatureSystem` protocol. Systems convert
between graphemes and feature bundles, handle class matching, and expose
distance calculations.

Built-in systems:

- `ipa`: compact categorical feature bundles
- `tresoldi`: broader categorical bundles preserving more modifiers
- `distinctive`: categorical features plus scalar conversions

### Registry

A `Registry` binds a dataset to one or more named systems. `distfeat` also
provides a lazily initialized default global registry so common use stays
simple.

### Geometry

`distfeat.geometry` provides a feature hierarchy based on the Clements & Hume
tradition. It is used for:

- feature-value distance
- sound distance
- category-aware grouping across systems

### Analysis

`distfeat.analysis` provides higher-level helpers that operate across systems:

- `features_to_graphemes(...)`
- `derive_class_features(...)`
- `minimal_matrix(...)`
- `tabulate_matrix(...)`
- `distance(...)`

## Recommended Usage

For most users:

```python
import distfeat

features = distfeat.get_features("a")
vowel_class = distfeat.get_class_features("V")
```

For isolated experiments or custom datasets:

```python
from distfeat import create_registry, load_dataset

dataset = load_dataset(directory="my_data")
registry = create_registry(dataset=dataset)
system = registry.get_system("ipa")
```

For analysis tasks:

```python
import distfeat

matrix = distfeat.minimal_matrix(["t", "d", "s"])
print(distfeat.tabulate_matrix(matrix))
```

## Guide Map

- [API](api.md)
- [Datasets](datasets.md)
- [Systems](systems.md)
- [Development](development.md)
