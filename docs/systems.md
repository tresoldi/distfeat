# Systems

`distfeat` currently ships with three built-in systems:

- `ipa`
- `tresoldi`
- `distinctive`

All three implement the `FeatureSystem` protocol and operate against a
`FeatureDataset`.

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

## Shared Behavior

Across systems:

- `class_features(...)` comes from the dataset class definitions
- `partial_match(...)` supports negative features such as `-stop`
- `add_features(...)` replaces conflicting values in the same category
- `feature_distance(...)` is geometry-backed

## Choosing a System

- use `ipa` for compact, stable categorical feature matching
- use `tresoldi` when you want richer categorical detail
- use `distinctive` when you need scalar representations for alignment,
  comparison, or downstream modeling
