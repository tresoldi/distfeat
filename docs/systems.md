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

## `CategoricalFeatureSystem` Base Class

`IPAFeatureSystem`, `TresoldiFeatureSystem`, and `DistinctiveFeatureSystem` all
inherit from `CategoricalFeatureSystem`, a regular (non-dataclass) base class
defined in `distfeat.systems.categorical`.

The base class provides:

- shared constants: `FEATURE_ALIASES`, `FEATURE_CATEGORIES`
- input/output normalization: `normalize_input_grapheme(...)`,
  `normalize_output_grapheme(...)`, `resolve_alias(...)`
- class table construction: `build_class_table(...)`
- all 15 shared methods from the `FeatureSystem` protocol: `list_graphemes`,
  `grapheme_to_features`, `grapheme_to_representation`, `features_to_grapheme`,
  `is_class`, `class_features`, `class_representation`, `add_features`,
  `partial_match`, `matches`, `feature_distance`, `segment_distance`,
  `sound_distance`, plus cached properties `_reverse_table` and `_class_table`

Each subclass only needs to define a `dataset` field, a `name` property, and a
`_grapheme_table` cached property with its system-specific parsing logic.
Frozen dataclasses can inherit from `CategoricalFeatureSystem` because the base
defines no dataclass fields.

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

Methodological assumptions:

- representation unit: categorical feature sets from parsed `sounds.tsv` labels
- matching semantics: subset/partial matching with optional negative features
- distance semantics: geometry-based categorical distance
- uncertainty handling: no explicit uncertainty model; absence means feature not present
- best for: compact inventory queries and interpretable rule-oriented analysis

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

Methodological assumptions:

- representation unit: broader categorical feature sets preserving more descriptors
- matching semantics: same categorical partial matching model as `ipa`
- distance semantics: same geometry-backed categorical distance model
- uncertainty handling: no explicit uncertainty states
- best for: exploratory work where richer categorical detail is preferred over compactness

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

Methodological assumptions:

- representation unit: categorical features plus derived scalar dimensions
- matching semantics: categorical matching for queries; scalar space used for distance
- distance semantics: weighted scalar-dimension distance grounded in geometry node depth
- uncertainty handling: missing dimensions are treated as neutral (`0.0`)
- best for: numeric comparison/modeling workflows needing stable scalar embeddings

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

Methodological assumptions:

- representation unit: native multi-state valued features (`+`, `-`, `n`, `.`, `o`, `x`)
- matching semantics: key/value matching over native valued representations
- distance semantics: mismatch ratio over comparable non-`.` features
- uncertainty handling: `.` is treated as underspecified and excluded from comparables
- best for: work that needs explicit underspecification and multi-state segment tables

Uncertainty controls:

- `features_to_graphemes(..., valued_dot_policy=...)` exposes wildcard policies for `.`
- `distance(..., valued_dot_policy=...)` exposes `ignore` / `partial` / `strict` handling
- `valued_matches(...)` and `valued_distance(...)` expose the same controls directly

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

## Cross-System Caveats

- results are not methodologically interchangeable across systems
- feature labels with similar names may play different operational roles by system
- `pbase-*` outputs should not be interpreted as categorical feature sets
- if comparing runs across studies, report system name and version explicitly
