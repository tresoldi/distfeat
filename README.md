# distfeat

`distfeat` is a standalone Python package for phonological feature systems.

It provides:

- phonological feature datasets
- feature system registries
- feature geometry and distance logic
- built-in systems: `ipa`, `tresoldi`, and `distinctive`

This package is the standalone home for the feature subsystem previously extracted from `alteruphono`.

## Scope

`distfeat` owns:

- bundled TSV datasets (`sounds.tsv`, `classes.tsv`, `features.tsv`)
- user dataset loading from directories, paths, or in-memory rows
- the `FeatureSystem` protocol
- explicit registries plus a lazy default global registry
- the Clements & Hume style feature geometry tree
- built-in systems for categorical and scalar feature representations

`distfeat` does not define a sound object. Consumers such as `alteruphono` can
map `distfeat` feature lookups into their own domain-specific dataclasses.

## Installation

Primary install path after the repository split:

```bash
pip install distfeat
```

Requires Python 3.12+. Runtime dependencies are intentionally empty.

Development install after the split:

```bash
git clone https://github.com/tresoldi/distfeat.git
cd distfeat
pip install -e ".[dev]"
```

## Quick Start

These examples assume the standalone package is installed in the normal way.

```python
import distfeat

# Built-in registry
print(distfeat.list_systems())
# ['ipa', 'tresoldi', 'distinctive']

# Top-level helpers
print(distfeat.get_features("p"))
print(distfeat.get_class_features("V"))

# Use a specific system
ipa = distfeat.get_system("ipa")
print(ipa.grapheme_to_features("a"))
print(ipa.features_to_grapheme(frozenset({"consonant", "voiced", "bilabial", "stop"})))
```

## Custom Dataset Example

```python
from distfeat import create_registry, load_dataset

dataset = load_dataset(directory="my_feature_data")
registry = create_registry(dataset=dataset)

features = registry.get_system("ipa").grapheme_to_features("k")
```

## Distinctive Scalars

```python
from distfeat import DistinctiveFeatureSystem, load_builtin_dataset

system = DistinctiveFeatureSystem(dataset=load_builtin_dataset())
scalars = system.grapheme_to_scalars("a")
print(scalars)
```

## Documentation

- `docs/index.md` for the package overview
- `docs/api.md` for the public API
- `docs/datasets.md` for dataset loading
- `docs/systems.md` for built-in systems
- `docs/development.md` for implementation constraints

## Relationship to alteruphono

`alteruphono` should be treated as a consumer of `distfeat`, not the owner of
the feature subsystem. After the split, `alteruphono` will depend on the
published `distfeat` package rather than carrying its own internal feature
implementation.
