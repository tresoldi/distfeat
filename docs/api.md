# API

The public API is intentionally small and functional-first.

## Top-Level Exports

The package root exposes the main user-facing API:

```python
import distfeat
```

Main exports:

- analysis APIs:
  - `FeatureMatrix`
  - `features_to_graphemes(...)`
  - `derive_class_features(...)`
  - `minimal_matrix(...)`
  - `tabulate_matrix(...)`
  - `distance(...)`
- dataset APIs:
  - `FeatureDataset`
  - `load_builtin_dataset()`
  - `load_dataset(...)`
  - `dataset_from_rows(...)`
- registry APIs:
  - `Registry`
  - `create_registry(...)`
  - `get_registry()`
  - `set_registry(...)`
  - `reset_registry()`
  - `register(...)`
  - `get_system(...)`
  - `list_systems()`
  - `set_default(...)`
- convenience helpers:
  - `get_features(...)`
  - `get_class_features(...)`
  - `is_class(...)`
  - `features_to_grapheme(...)`
  - `add_features(...)`
  - `partial_match(...)`
  - `feature_distance(...)`
  - `sound_distance(...)`
- protocol and geometry:
  - `FeatureSystem`
  - `FeatureNode`
  - `GeometryNode`
  - `DEFAULT_GEOMETRY`
- built-in systems:
  - `IPAFeatureSystem`
  - `TresoldiFeatureSystem`
  - `DistinctiveFeatureSystem`

## Functional Helpers

Use these for the default lazy global registry:

```python
import distfeat

features = distfeat.get_features("p")
class_features = distfeat.get_class_features("V")
is_class = distfeat.is_class("C")
```

These call through the current default system unless you pass `system="..."`.

## Registry API

The explicit registry API is the clean boundary for custom datasets and
isolated state:

```python
from distfeat import create_registry, load_dataset

dataset = load_dataset(directory="my_data")
registry = create_registry(dataset=dataset)

system = registry.get_system("ipa")
```

`Registry` methods:

- `register(name, system)`
- `get_system(name=None)`
- `list_systems()`
- `set_default(name)`

## Dataset API

`FeatureDataset` is a frozen dataclass with:

- `sounds`
- `classes`
- `features`

Derived properties:

- `feature_values`
- `class_graphemes`
- `class_features`

## System Protocol

All systems implement:

```python
class FeatureSystem(Protocol):
    @property
    def name(self) -> str: ...
    def grapheme_to_features(self, grapheme: str) -> frozenset[str] | None: ...
    def features_to_grapheme(self, features: frozenset[str]) -> str | None: ...
    def is_class(self, grapheme: str) -> bool: ...
    def class_features(self, grapheme: str) -> frozenset[str] | None: ...
    def add_features(self, base: frozenset[str], added: frozenset[str]) -> frozenset[str]: ...
    def partial_match(self, pattern: frozenset[str], target: frozenset[str]) -> bool: ...
    def feature_distance(self, feat_a: str, feat_b: str) -> float: ...
    def sound_distance(self, feats_a: frozenset[str], feats_b: frozenset[str]) -> float: ...
```

The `distinctive` system also exposes scalar-specific methods beyond the base
protocol.

## Geometry API

`distfeat.geometry` exports:

- `FeatureNode`
- `GeometryNode`
- `DEFAULT_GEOMETRY`
- `FEATURE_TO_GEOMETRY_NODE`

Typical usage:

```python
from distfeat.geometry import DEFAULT_GEOMETRY

distance = DEFAULT_GEOMETRY.feature_distance("voiced", "voiceless")
```

## Analysis API

The analysis layer is exposed at package root and implemented in
`distfeat.analysis`.

### `features_to_graphemes(...)`

Returns all graphemes matching a feature query. By default this uses partial
matching with the selected system's semantics.

```python
import distfeat

matches = distfeat.features_to_graphemes(frozenset({"consonant", "-voiced"}))
```

### `derive_class_features(...)`

Returns the strict shared feature intersection for a set of graphemes.

```python
common = distfeat.derive_class_features(["t", "d"])
```

### `minimal_matrix(...)`

Returns a `FeatureMatrix` with the smallest distinguishing column set for the
requested graphemes.

- `ipa` / `tresoldi`: categorical boolean matrix
- `distinctive`: scalar dimension matrix

### `tabulate_matrix(...)`

Renders a `FeatureMatrix` as `plain` or `markdown`.

### `distance(...)`

Computes grapheme-to-grapheme distance directly.

It can either:

- resolve graphemes through a system and use that system's native distance
- use an explicitly provided precomputed nested-dict distance matrix
