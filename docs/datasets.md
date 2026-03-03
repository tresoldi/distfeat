# Datasets

A `FeatureDataset` is the data backbone for all feature systems.

## Built-In Dataset

`distfeat` ships with bundled TSV data:

- `sounds.tsv`
- `classes.tsv`
- `features.tsv`

Load it with:

```python
from distfeat import load_builtin_dataset

dataset = load_builtin_dataset()
```

This returns a frozen `FeatureDataset` instance.

## Load From a Directory

If your data lives in a directory using the same filenames:

```python
from distfeat import load_dataset

dataset = load_dataset(directory="my_data")
```

Expected files:

- `my_data/sounds.tsv`
- `my_data/classes.tsv`
- `my_data/features.tsv`

## Load From Explicit Paths

You can also provide file paths directly:

```python
from distfeat import load_dataset

dataset = load_dataset(
    sounds_path="custom/sounds.tsv",
    classes_path="custom/classes.tsv",
    features_path="custom/features.tsv",
)
```

## Build From In-Memory Rows

For programmatic generation or tests:

```python
from distfeat import dataset_from_rows

dataset = dataset_from_rows(
    sounds={"a": "open front vowel"},
    classes={"V": ("vowel", "vowel", ["a"])},
    features=[("open", "height"), ("front", "centrality")],
)
```

## Required TSV Shapes

### `sounds.tsv`

Columns:

- `GRAPHEME`
- `NAME`

### `classes.tsv`

Columns:

- `SOUND_CLASS`
- `DESCRIPTION`
- `FEATURES`
- `GRAPHEMES`

`GRAPHEMES` uses `|` as the internal separator.

### `features.tsv`

Columns:

- `VALUE`
- `FEATURE`

## Derived Views

`FeatureDataset` exposes useful computed properties:

- `feature_values`: maps a feature name to all known values
- `class_graphemes`: maps a sound class to its grapheme set
- `class_features`: maps a sound class to its raw feature string

These are enough to support the current built-in systems without adding more
dataset abstraction.
