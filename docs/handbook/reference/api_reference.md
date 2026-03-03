# API Reference

This page documents the complete public API surface of distfeat, organized by
module. All items listed here are importable directly from `distfeat`.

```python
import distfeat
```

---

## Registry and System Management

These functions manage the global registry of feature systems and provide
access to individual systems.

### `list_systems()`

Return the names of all registered feature systems.

```python
distfeat.list_systems()
# ['distinctive', 'ipa', 'pbase-hc', 'pbase-jfh', 'pbase-spe', 'pbase-uftc', 'tresoldi']
```

**Returns:** `list[str]`

### `get_system(name=None)`

Retrieve a registered feature system by name. If `name` is `None`, the
default system (initially `"ipa"`) is returned.

```python
sys = distfeat.get_system("distinctive")
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str \| None` | `None` | System name, or `None` for the default |

**Returns:** `FeatureSystem`

**Raises:** `KeyError` if the name is not registered.

### `set_default(name)`

Change the default system used by convenience helpers.

```python
distfeat.set_default("tresoldi")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Name of a registered system |

### `register(name, system)`

Register a new feature system under the given name.

```python
distfeat.register("my_system", my_custom_system)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Name to register under |
| `system` | `FeatureSystem` | System instance |

### `create_registry(dataset=None, *, register_builtin=True, default_system="ipa")`

Create a new, isolated `Registry`. Useful for testing or working with
custom datasets.

```python
reg = distfeat.create_registry(default_system="tresoldi")
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | `FeatureDataset \| None` | `None` | Custom dataset; `None` uses built-in |
| `register_builtin` | `bool` | `True` | Whether to register the 7 built-in systems |
| `default_system` | `str` | `"ipa"` | Name of the default system |

**Returns:** `Registry`

### `get_registry()`

Return the lazily initialized global registry.

**Returns:** `Registry`

### `set_registry(registry)`

Replace the global registry with a custom one.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `registry` | `Registry` | Replacement registry |

### `reset_registry()`

Reset the global registry so it will be re-initialized on next access.

---

## Feature Lookup

Convenience helpers that delegate to the default (or named) system.

### `get_features(grapheme, *, system=None)`

Return the categorical feature set for a grapheme.

```python
distfeat.get_features("p")
# frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `grapheme` | `str` | | IPA grapheme |
| `system` | `str \| None` | `None` | System name, or `None` for default |

**Returns:** `frozenset[str] | None`

### `get_representation(grapheme, *, system=None)`

Return the native representation for a grapheme. For categorical systems
this is a `CategoricalFeatures`; for valued systems, a `ValuedFeatures`.

```python
distfeat.get_representation("p")                    # CategoricalFeatures
distfeat.get_representation("p", system="pbase-hc") # ValuedFeatures
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `grapheme` | `str` | | IPA grapheme |
| `system` | `str \| None` | `None` | System name, or `None` for default |

**Returns:** `CategoricalFeatures | ValuedFeatures | None`

### `is_class(grapheme, *, system=None)`

Check whether a symbol is a predefined sound class (e.g., `"S"` for stops,
`"V"` for vowels).

```python
distfeat.is_class("S")  # True
distfeat.is_class("p")  # False
```

**Returns:** `bool`

### `get_class_features(grapheme, *, system=None)`

Return the categorical feature set defining a sound class.

```python
distfeat.get_class_features("S")
# frozenset({'consonant', 'stop'})
```

**Returns:** `frozenset[str] | None`

### `get_class_representation(grapheme, *, system=None)`

Return the native representation for a sound class.

**Returns:** `CategoricalFeatures | ValuedFeatures | None`

### `features_to_grapheme(features, *, system=None)`

Return the grapheme whose features exactly match the given set.

```python
distfeat.features_to_grapheme(frozenset({"consonant", "voiceless", "bilabial", "stop"}))
# "p"
```

**Returns:** `str | None`

---

## Feature Queries and Matching

### `features_to_graphemes(query, *, system=None, exact=False)`

Return all graphemes satisfying a feature query. For categorical systems,
`query` is a `frozenset[str]`. For valued systems, `query` is a
`dict[str, FeatureState | str]`.

```python
distfeat.features_to_graphemes(frozenset({"consonant", "stop", "voiceless"}))
# ['p', 't', 'k', ...]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `frozenset[str] \| dict` | | Feature query |
| `system` | `str \| None` | `None` | System name |
| `exact` | `bool` | `False` | If `True`, require exact match |

**Returns:** `list[str]`

### `partial_match(pattern, target, *, system=None)`

Check whether a feature pattern is a subset of a target. Supports negative
features: a pattern element `"-voiced"` requires `"voiced"` to be absent
from the target.

```python
pattern = frozenset({"consonant", "-voiced"})
target = frozenset({"consonant", "voiceless", "bilabial", "stop"})
distfeat.partial_match(pattern, target)  # True
```

**Returns:** `bool`

### `matches(pattern, target, *, system=None)`

Check whether a pattern matches a target using the system's native matching
semantics.

**Returns:** `bool`

### `derive_class_features(graphemes, *, system=None)`

Derive the strict shared feature intersection of a set of graphemes.

```python
distfeat.derive_class_features(["p", "t", "k"])
# frozenset({'consonant', 'voiceless', 'stop'})
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `graphemes` | `list[str] \| tuple[str, ...]` | Graphemes to intersect |
| `system` | `str \| None` | System name |

**Returns:** `frozenset[str]` (categorical) or `dict[str, FeatureState]` (valued)

### `add_features(base, added, *, system=None)`

Add features to a feature set with category-aware replacement. If the added
feature belongs to the same category as an existing feature, the existing
feature is replaced.

```python
features_p = distfeat.get_features("p")
features_b = distfeat.add_features(features_p, frozenset({"voiced"}))
# Replaces "voiceless" with "voiced" (both in phonation category)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `base` | `frozenset[str]` | Base feature set |
| `added` | `frozenset[str]` | Features to add |
| `system` | `str \| None` | System name |

**Returns:** `frozenset[str]`

---

## Distance

### `distance(grapheme_a, grapheme_b, *, system=None, precomputed=None)`

Return the distance between two graphemes. If `precomputed` is provided,
look up the pair in the dictionary first.

```python
distfeat.distance("p", "b")  # ~0.08
distfeat.distance("p", "t")  # ~0.17
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `grapheme_a` | `str` | | First grapheme |
| `grapheme_b` | `str` | | Second grapheme |
| `system` | `str \| None` | `None` | System name |
| `precomputed` | `dict \| None` | `None` | Pre-computed distance lookup |

**Returns:** `float`

### `sound_distance(feats_a, feats_b, *, system=None)`

Return the distance between two categorical feature sets using geometry
weighting.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `feats_a` | `frozenset[str]` | First feature set |
| `feats_b` | `frozenset[str]` | Second feature set |
| `system` | `str \| None` | System name |

**Returns:** `float`

### `segment_distance(a, b, *, system=None)`

Return the distance between two native representations.

**Returns:** `float`

### `feature_distance(feat_a, feat_b, *, system=None)`

Return the tree-edge distance between two individual feature values.

```python
distfeat.feature_distance("voiced", "voiceless")  # small
distfeat.feature_distance("voiced", "bilabial")   # large
```

**Returns:** `float`

---

## Matrices

### `minimal_matrix(graphemes, *, system=None)`

Return a minimal distinguishing feature matrix for a set of graphemes. The
matrix contains the smallest set of features that uniquely identifies each
grapheme.

```python
matrix = distfeat.minimal_matrix(["p", "b"])
```

**Returns:** `FeatureMatrix`

### `tabulate_matrix(matrix, *, format="plain")`

Render a `FeatureMatrix` as a formatted string.

```python
print(distfeat.tabulate_matrix(matrix))
print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `matrix` | `FeatureMatrix` | | Matrix to render |
| `format` | `str` | `"plain"` | `"plain"` or `"markdown"` |

**Returns:** `str`

---

## Dataset

### `load_builtin_dataset()`

Load the bundled TSV dataset. The result is cached.

**Returns:** `FeatureDataset`

### `load_dataset(directory=None, *, sounds_path=None, classes_path=None, features_path=None)`

Load a dataset from a directory or explicit file paths. If all paths are
`None`, the built-in dataset is loaded.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `directory` | `str \| Path \| None` | `None` | Directory containing TSV files |
| `sounds_path` | `str \| Path \| None` | `None` | Path to sounds.tsv |
| `classes_path` | `str \| Path \| None` | `None` | Path to classes.tsv |
| `features_path` | `str \| Path \| None` | `None` | Path to features.tsv |

**Returns:** `FeatureDataset`

### `dataset_from_rows(*, sounds, classes, features)`

Build a dataset directly from in-memory data.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `sounds` | `Mapping[str, str]` | GRAPHEME → NAME |
| `classes` | `Mapping[str, tuple[str, str, list[str]]]` | SOUND_CLASS → (DESCRIPTION, FEATURES, GRAPHEMES) |
| `features` | `list[tuple[str, str]]` | (VALUE, FEATURE) pairs |

**Returns:** `FeatureDataset`

---

## Data Types

### `CategoricalFeatures`

A frozen dataclass wrapping a `frozenset[str]` of categorical feature
labels.

```python
from distfeat import CategoricalFeatures
cf = CategoricalFeatures(frozenset({"consonant", "stop", "voiced"}))
cf.values  # frozenset({'consonant', 'stop', 'voiced'})
```

**Fields:** `values: frozenset[str]`

### `ValuedFeatures`

A frozen dataclass wrapping a `dict[str, FeatureState]` of named feature
values.

```python
from distfeat import ValuedFeatures, FeatureState
vf = ValuedFeatures({"voice": FeatureState.POSITIVE, "nasal": FeatureState.NEGATIVE})
vf.values  # {'voice': FeatureState.POSITIVE, 'nasal': FeatureState.NEGATIVE}
```

**Fields:** `values: dict[str, FeatureState]`

### `FeatureState`

A `StrEnum` representing symbolic feature values in multi-state systems.

| Member | Value | Meaning |
|--------|-------|---------|
| `POSITIVE` | `"+"` | Feature is positively specified |
| `NEGATIVE` | `"-"` | Feature is negatively specified |
| `DOT` | `"."` | Unspecified or conflicting |
| `N` | `"n"` | System-specific neutral |
| `O` | `"o"` | System-specific value |
| `X` | `"x"` | System-specific value |

### `FeatureRepresentation`

Type alias: `CategoricalFeatures | ValuedFeatures`.

### `FeatureMatrix`

A frozen dataclass representing a minimal feature matrix.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `columns` | `tuple[str, ...]` | Feature names (column headers) |
| `rows` | `Mapping[str, tuple[object, ...]]` | Grapheme → feature values |
| `system` | `str` | Name of the source system |
| `mode` | `str` | `"categorical"`, `"valued"`, or `"scalar"` |

### `FeatureDataset`

A frozen dataclass containing the three TSV tables.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `sounds` | `dict[str, str]` | GRAPHEME → NAME |
| `classes` | `dict[str, tuple[str, str, list[str]]]` | SOUND_CLASS → (DESCRIPTION, FEATURES, GRAPHEMES) |
| `features` | `list[tuple[str, str]]` | (VALUE, FEATURE) pairs |

**Properties:** `feature_values`, `class_graphemes`, `class_features`

---

## Geometry

### `DEFAULT_GEOMETRY`

The Clements & Hume (1995) feature geometry tree, a `GeometryNode`
instance. See the [Feature Catalog](feature_catalog.md) for the full tree
structure.

### `GeometryNode`

A frozen dataclass representing an internal node in the geometry tree.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Node name (e.g., `"Laryngeal"`, `"Place"`) |
| `children` | `tuple[GeometryNode \| FeatureNode, ...]` | Child nodes |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `all_features()` | `frozenset[str]` | All leaf positive/negative values |
| `find_feature(value)` | `FeatureNode \| None` | Lookup by feature value |
| `find_parent(value)` | `GeometryNode \| None` | Parent node of a feature |
| `siblings_of(value)` | `frozenset[str]` | Sibling feature values |
| `feature_distance(a, b)` | `int` | Tree-edge distance between values |
| `sound_distance(feats_a, feats_b)` | `float` | Normalized set distance |

### `FeatureNode`

A frozen dataclass representing a leaf feature in the geometry tree.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Feature name (e.g., `"voice"`, `"nasal"`) |
| `positive` | `str` | Positive value (e.g., `"voiced"`) |
| `negative` | `str` | Negative value (e.g., `"voiceless"`), or `""` |

---

## Feature System Classes

### `IPAFeatureSystem`

Categorical system derived from IPA sound names. Default system.

### `TresoldiFeatureSystem`

Categorical system with broader descriptive labels.

### `DistinctiveFeatureSystem`

Categorical system with an additional scalar layer.

**Extra methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `grapheme_to_scalars(grapheme)` | `dict[str, float] \| None` | Scalar dimension values |
| `features_to_scalars(features)` | `dict[str, float]` | Convert features to scalars |
| `scalars_to_features(scalars)` | `frozenset[str]` | Convert scalars to features |

### `PBaseFeatureSystem`

Multi-state valued system for P-base families. Instantiated with a
`family` parameter: `"hc"`, `"jfh"`, `"spe"`, or `"uftc"`.

### `Registry`

Mutable container for named feature systems.

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `register(name, system)` | | Add a system |
| `get_system(name=None)` | `FeatureSystem` | Fetch by name |
| `list_systems()` | `list[str]` | All registered names |
| `set_default(name)` | | Change the default |

---

## Protocol

### `FeatureSystem`

The structural protocol that all feature systems must implement. See the
source in `distfeat.protocol` for the full method signatures. Any object
satisfying this protocol can be registered and used interchangeably.
