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
- export APIs:
  - `export_matrix(...)`
  - `export_distances(...)`
  - `export_class_features(...)`
- dataset APIs:
  - `FeatureDataset`
  - `load_builtin_dataset()`
  - `load_dataset(...)`
  - `dataset_from_rows(...)`
  - `DatasetAuditReport`
  - `audit_dataset(...)`
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
  - `get_representation(...)`
  - `get_class_features(...)`
  - `get_class_representation(...)`
  - `is_class(...)`
  - `features_to_grapheme(...)`
  - `add_features(...)`
  - `matches(...)`
  - `partial_match(...)`
  - `feature_distance(...)`
  - `segment_distance(...)`
  - `sound_distance(...)`
- protocol and geometry:
  - `FeatureSystem`
  - `FeatureState`
  - `CategoricalFeatures`
  - `ValuedFeatures`
  - `FeatureNode`
  - `GeometryNode`
  - `DEFAULT_GEOMETRY`
- built-in systems:
  - `IPAFeatureSystem`
  - `TresoldiFeatureSystem`
  - `DistinctiveFeatureSystem`
  - `PBaseFeatureSystem`

The `distfeat.systems` subpackage additionally exports `CategoricalFeatureSystem`,
the shared base class for `IPAFeatureSystem`, `TresoldiFeatureSystem`, and
`DistinctiveFeatureSystem`.

## Functional Helpers

Use these for the default lazy global registry:

```python
import distfeat

features = distfeat.get_features("p")
class_features = distfeat.get_class_features("V")
valued = distfeat.get_representation("a", system="pbase-hc")
is_class = distfeat.is_class("C")
```

These call through the current default system unless you pass `system="..."`.

For new code, prefer the native-representation helpers:

- `get_representation(...)` over `get_features(...)`
- `get_class_representation(...)` over `get_class_features(...)`
- `matches(...)` over `partial_match(...)`
- `segment_distance(...)` over `sound_distance(...)`

The older set-based helpers remain useful for categorical systems, but they
are compatibility-oriented and are not the full surface for valued systems such
as `pbase-*`.

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
    @property
    def representation_kind(self) -> str: ...
    def list_graphemes(self) -> tuple[str, ...]: ...
    def grapheme_to_representation(self, grapheme: str) -> FeatureRepresentation | None: ...
    def grapheme_to_features(self, grapheme: str) -> frozenset[str] | None: ...
    def features_to_grapheme(self, features: object) -> str | None: ...
    def is_class(self, grapheme: str) -> bool: ...
    def class_representation(self, grapheme: str) -> FeatureRepresentation | None: ...
    def class_features(self, grapheme: str) -> frozenset[str] | None: ...
    def add_features(self, base: frozenset[str], added: frozenset[str]) -> frozenset[str]: ...
    def matches(self, pattern: object, target: object) -> bool: ...
    def partial_match(self, pattern: frozenset[str], target: frozenset[str]) -> bool: ...
    def feature_distance(self, feat_a: str, feat_b: str) -> float: ...
    def segment_distance(self, a: object, b: object) -> float: ...
    def sound_distance(self, feats_a: frozenset[str], feats_b: frozenset[str]) -> float: ...
```

The three categorical systems (`ipa`, `tresoldi`, `distinctive`) all inherit
from `CategoricalFeatureSystem`, which implements the full protocol. Each
subclass only overrides `name` and `_grapheme_table`. The `distinctive` system
additionally exposes scalar-specific methods beyond the base protocol, and the
P-base-derived systems use `ValuedFeatures` plus `FeatureState` for native
multi-state feature values.

In practice:

- categorical systems (`ipa`, `tresoldi`, `distinctive`) expose
  `CategoricalFeatures`
- P-base-derived systems expose `ValuedFeatures`

When a system has a richer native representation, that representation should be
treated as the canonical API for new code.

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

For valued systems such as `pbase-hc`, the query is a dictionary of feature
names to symbolic states:

```python
matches = distfeat.features_to_graphemes({"syllabic": "+"}, system="pbase-hc")
```

### `derive_class_features(...)`

Returns the strict shared feature intersection for a set of graphemes.

```python
common = distfeat.derive_class_features(["t", "d"])
valued_common = distfeat.derive_class_features(["t", "d"], system="pbase-hc")
```

### `minimal_matrix(...)`

Returns a `FeatureMatrix` with the smallest distinguishing column set for the
requested graphemes.

- `ipa` / `tresoldi`: categorical boolean matrix
- `distinctive`: scalar dimension matrix
- `pbase-*`: valued matrix using `FeatureState` cells

### `tabulate_matrix(...)`

Renders a `FeatureMatrix` as `plain` or `markdown`.

### `distance(...)`

Computes grapheme-to-grapheme distance directly.

It can either:

- resolve graphemes through a system and use that system's native distance
- use an explicitly provided precomputed nested-dict distance matrix

## Export APIs

The export helpers provide stable TSV/CSV/JSON serialization for common
analysis outputs.

- `export_matrix(matrix, path, format=None)`
- `export_distances(distances, path, format=None)`
- `export_class_features(features, path, format=None)`

Format behavior:

- if `format` is omitted, the function infers it from the file extension
- supported formats are `json`, `csv`, and `tsv`
