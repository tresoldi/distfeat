# Systems

`distfeat` currently ships with seven built-in systems:

- `ipa`
- `tresoldi`
- `distinctive`
- `pbase-hc`
- `pbase-jfh`
- `pbase-spe`
- `pbase-uftc`

All seven implement the `FeatureSystem` protocol and operate against a
`FeatureDataset`.

For new code, the native representation methods are the preferred entry point:

- `grapheme_to_representation(...)`
- `class_representation(...)`
- `matches(...)`
- `segment_distance(...)`

The older set-based methods remain first-class for categorical systems, but
they are compatibility-oriented and intentionally do not capture the full
surface of valued systems such as `pbase-*`.

## `ipa`

`IPAFeatureSystem` provides a compact categorical representation derived from
the descriptive `NAME` field in `sounds.tsv`.

Characteristics:

- keeps a focused feature subset
- supports sound classes from `classes.tsv`
- supports category-aware feature replacement through `add_features(...)`
- uses the shared geometry-based distance functions

Typical use:

```python
from distfeat import IPAFeatureSystem, load_builtin_dataset

system = IPAFeatureSystem(dataset=load_builtin_dataset())
print(system.grapheme_to_features("p"))
```

## `tresoldi`

`TresoldiFeatureSystem` parses a broader categorical bundle from the same
dataset and preserves more descriptive material from the sound names.

Characteristics:

- wider categorical coverage than `ipa`
- retains more modifiers and descriptive distinctions
- shares class handling and distance behavior with the common framework

Typical use:

```python
from distfeat import TresoldiFeatureSystem, load_builtin_dataset

system = TresoldiFeatureSystem(dataset=load_builtin_dataset())
print(system.grapheme_to_features("a"))
```

## `distinctive`

`DistinctiveFeatureSystem` keeps categorical compatibility but also exposes a
scalar feature view.

Extra public methods:

- `grapheme_to_scalars(grapheme)`
- `features_to_scalars(features)`
- `scalars_to_features(scalars)`

Characteristics:

- uses named scalar dimensions
- maps categorical feature bundles into weighted scalar space
- computes sound distance from scalar dimensions rather than only the shared
  categorical geometry wrapper

Typical use:

```python
from distfeat import DistinctiveFeatureSystem, load_builtin_dataset

system = DistinctiveFeatureSystem(dataset=load_builtin_dataset())
print(system.grapheme_to_scalars("a"))
```

## `pbase-*`

The P-base-derived systems use the package's native multi-state representation
instead of a simple categorical set.

Available families:

- `pbase-hc`
- `pbase-jfh`
- `pbase-spe`
- `pbase-uftc`

Characteristics:

- bundle a derived segment table based on the P-base data files
- preserve symbolic feature states (`+`, `-`, `n`, `.`, `o`, `x`)
- expose native `ValuedFeatures` objects
- support dict-based matching, matrix construction, and direct distance
- merge duplicate source rows conservatively:
  identical duplicates collapse, and conflicting cells are downgraded to `.`

Typical use:

```python
import distfeat

system = distfeat.get_system("pbase-hc")
print(system.grapheme_to_representation("a"))
print(distfeat.features_to_graphemes({"syllabic": "+"}, system="pbase-hc"))
```

## Shared Behavior

Across systems:

- `class_features(...)` comes from the dataset class definitions
- `partial_match(...)` supports negative features such as `-stop`
- `add_features(...)` replaces conflicting values in the same category
- `feature_distance(...)` is geometry-backed
- P-base-derived systems instead expose native multi-state matching and a
  direct symbolic-state distance

The analysis helpers work across all built-in systems:

- `features_to_graphemes(...)` uses each system's matching semantics
- `derive_class_features(...)` derives shared feature intersections
- `minimal_matrix(...)` uses categorical columns for `ipa`/`tresoldi`
- `minimal_matrix(...)` uses scalar dimensions for `distinctive`
- `minimal_matrix(...)` uses symbolic valued columns for `pbase-*`

## Choosing a System

- use `ipa` for compact, stable categorical feature matching
- use `tresoldi` when you want richer categorical detail
- use `distinctive` when you need scalar representations for alignment,
  comparison, or downstream modeling
- use `pbase-*` when you need native multi-state feature tables derived from
  the bundled P-base data
