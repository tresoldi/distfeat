# distfeat

`distfeat` is a standalone Python package for manipulating phonological
features.

It provides:

- bundled phonological feature datasets
- pluggable feature systems
- feature geometry and distance functions
- query and analysis helpers for graphemes and feature sets

`distfeat` is dependency-free at runtime and is the standalone home for the
feature subsystem extracted from `alteruphono`.

## Installation

Install from PyPI:

```bash
pip install distfeat
```

Requires Python 3.12+.

Development install:

```bash
git clone https://github.com/tresoldi/distfeat.git
cd distfeat
pip install -e ".[dev]"
```

## Core Concepts

The package is organized around:

- a bundled `FeatureDataset`
- a lazy default registry plus explicit `Registry` instances
- built-in systems:
  - `ipa`
  - `tresoldi`
  - `distinctive`

The package does not define a `Sound` object. It works directly with graphemes,
feature bundles, scalar dimensions, and matrices.

## Quick Start

```python
import distfeat

# Built-in systems
print(distfeat.list_systems())
# ['ipa', 'tresoldi', 'distinctive']

# Basic grapheme lookup
print(distfeat.get_features("p"))
# frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})

# Predefined sound classes
print(distfeat.get_class_features("V"))
# frozenset({'vowel'})

# Direct grapheme distance
print(distfeat.distance("a", "e"))
```

## Working With Systems

You can use the lazy default registry through top-level helpers, or you can
work with a specific system object.

```python
import distfeat

ipa = distfeat.get_system("ipa")
tresoldi = distfeat.get_system("tresoldi")
distinctive = distfeat.get_system("distinctive")

print(ipa.grapheme_to_features("a"))
print(tresoldi.grapheme_to_features("a"))
print(distinctive.grapheme_to_features("a"))
```

Exact reverse lookup is available when a feature bundle maps directly to a
known grapheme:

```python
ipa = distfeat.get_system("ipa")

grapheme = ipa.features_to_grapheme(
    frozenset({"consonant", "voiced", "bilabial", "stop"})
)
print(grapheme)
# 'b'
```

## Feature Queries

### Find Graphemes Matching a Feature Set

Use `features_to_graphemes(...)` to retrieve all graphemes satisfying a
feature query.

By default, matching is partial and uses the semantics of the selected system.

```python
import distfeat

# All vowels in the default system
vowels = distfeat.features_to_graphemes(frozenset({"vowel"}))
print(vowels[:10])

# Voiceless consonants
voiceless_consonants = distfeat.features_to_graphemes(
    frozenset({"consonant", "-voiced"})
)
print(voiceless_consonants[:10])
```

You can also force exact matching:

```python
import distfeat

ipa = distfeat.get_system("ipa")
features = ipa.grapheme_to_features("a")
print(distfeat.features_to_graphemes(features, exact=True))
```

### Derive Shared Class Features

Use `derive_class_features(...)` to compute the strict shared feature
intersection of a set of graphemes.

```python
import distfeat

print(distfeat.derive_class_features(["t", "d"]))
# frozenset({'consonant', 'alveolar', 'stop', ...})

print(distfeat.derive_class_features(["t", "d", "s"]))
# fewer shared features than the pair above
```

## Minimal Distinguishing Matrices

Use `minimal_matrix(...)` to compute the smallest feature set needed to
distinguish a given list of graphemes.

```python
import distfeat

matrix = distfeat.minimal_matrix(["t", "d"], system="ipa")
print(matrix.columns)
print(matrix.rows)
```

For `ipa` and `tresoldi`, the matrix is categorical and boolean. For
`distinctive`, it uses scalar dimensions.

```python
import distfeat

matrix = distfeat.minimal_matrix(["t", "d", "s"], system="ipa")
print(distfeat.tabulate_matrix(matrix))
```

Example plain-text output:

```text
grapheme | continuant | voiced
---------+------------+-------
t        | False      | False
d        | False      | True
s        | True       | False
```

Markdown output is also supported:

```python
print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

## Distinctive Scalars

The `distinctive` system also exposes scalar representations.

```python
from distfeat import DistinctiveFeatureSystem, load_builtin_dataset

system = DistinctiveFeatureSystem(dataset=load_builtin_dataset())

print(system.grapheme_to_scalars("a"))
print(system.features_to_scalars(system.grapheme_to_features("a")))
print(system.scalars_to_features({"voice": 1.0, "labial": 1.0}))
```

## Distance

### System-Based Distance

The default `distance(...)` helper resolves graphemes through the selected
system and uses that system's native distance.

```python
import distfeat

print(distfeat.distance("a", "e"))
print(distfeat.distance("a", "u"))
print(distfeat.distance("p", "b"))
```

### Precomputed Distance Matrices

You can also supply a precomputed nested dictionary.

```python
import distfeat

precomputed = {
    "a": {"e": 1.5, "u": 2.0},
    "p": {"b": 0.5},
}

print(distfeat.distance("a", "e", precomputed=precomputed))
print(distfeat.distance("b", "p", precomputed=precomputed))
```

If a requested pair is missing from the precomputed matrix, the function raises
`KeyError`.

## Custom Datasets

### Load From a Directory

```python
from distfeat import create_registry, load_dataset

dataset = load_dataset(directory="my_feature_data")
registry = create_registry(dataset=dataset)
system = registry.get_system("ipa")

print(system.grapheme_to_features("k"))
```

Expected files in `my_feature_data/`:

- `sounds.tsv`
- `classes.tsv`
- `features.tsv`

### Build From In-Memory Rows

```python
from distfeat import create_registry, dataset_from_rows
from distfeat.systems.ipa import IPAFeatureSystem

dataset = dataset_from_rows(
    sounds={"a": "open front vowel", "p": "voiceless bilabial consonant stop"},
    classes={"V": ("vowel", "vowel", ["a"])},
    features=[("open", "height"), ("front", "centrality"), ("stop", "manner")],
)

registry = create_registry(dataset=dataset, register_builtin=False)
registry.register("ipa", IPAFeatureSystem(dataset))

print(registry.get_system("ipa").grapheme_to_features("a"))
```

## Explicit Registries

Use explicit registries when you want isolated state instead of the default
global registry.

```python
from distfeat import create_registry, load_builtin_dataset

registry = create_registry(dataset=load_builtin_dataset())
registry.set_default("tresoldi")

print(registry.get_system().name)
print(registry.list_systems())
```

## What The Package Does Not Do

The current package intentionally does not provide:

- a legacy `DistFeat` facade class
- the old binary/tristate feature-table interface
- `grapheme2features(..., t_values=False)` style `+/-/0` rendering
- vector output modes for feature tables or matrices
- a command-line interface
- ML-based distance training

The current public API is built around categorical feature bundles, scalar
dimensions for the `distinctive` system, and analysis helpers over those
representations.

## Documentation

- [docs/index.md](docs/index.md) for the package overview
- [docs/api.md](docs/api.md) for the public API
- [docs/datasets.md](docs/datasets.md) for dataset loading
- [docs/systems.md](docs/systems.md) for built-in systems
- [docs/development.md](docs/development.md) for implementation constraints

## Relationship to alteruphono

`alteruphono` should be treated as a consumer of `distfeat`, not the owner of
the feature subsystem.
