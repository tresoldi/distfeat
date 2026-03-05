# Chapter 6: Matrices and Geometry

<p class="chapter-subtitle">Minimal feature matrices and the Clements--Hume geometry tree</p>

A feature chart that lists every property of every segment in an
inventory is informative but unwieldy. What a working comparatist
usually needs is a *minimal* chart: the smallest set of features that
still tells every segment apart. `distfeat` computes these matrices
automatically. Behind the scenes, the matrix algorithm relies on a
**feature geometry tree** that organizes phonological features into a
hierarchy of articulatory nodes. This chapter introduces both tools and
shows how they interact.

---

## Minimal Matrices

The function `minimal_matrix` takes a list of graphemes and returns a
`FeatureMatrix` object whose columns are the smallest set of features
sufficient to distinguish every segment from every other.

### A two-segment matrix

The simplest case is a minimal pair. Two segments that differ in
exactly one feature need exactly one column:

```python
import distfeat

matrix = distfeat.minimal_matrix(["p", "b"])
print(matrix.columns)
# ('voiced',)
print(dict(matrix.rows))
# {'p': (False,), 'b': (True,)}
```

The single column `voiced` is enough: /p/ is `False`, /b/ is `True`.
No other feature is needed to tell them apart, so none appears.

### A four-segment matrix

Adding /t/ and /d/ introduces a place contrast alongside the voicing
contrast. The algorithm now selects two columns:

```python
import distfeat

matrix = distfeat.minimal_matrix(["p", "b", "t", "d"])
print(matrix.columns)
# ('alveolar', 'voiced')
print(dict(matrix.rows))
# {'p': (False, False), 'b': (False, True),
#  't': (True, False), 'd': (True, True)}
```

`alveolar` separates the coronals (/t/, /d/) from the labials (/p/,
/b/); `voiced` separates each voice pair. Together, the two features
produce four unique signatures, one per segment.

### The FeatureMatrix dataclass

`minimal_matrix` returns a frozen `FeatureMatrix` with four fields:

| Field | Type | Description |
| --- | --- | --- |
| `columns` | `tuple[str, ...]` | The selected distinguishing features |
| `rows` | `Mapping[str, tuple[object, ...]]` | Grapheme-to-values mapping |
| `system` | `str` | Name of the feature system used |
| `mode` | `str` | `"categorical"`, `"scalar"`, or `"valued"` |

The `mode` field records which representation layer produced the
matrix. By default, the IPA system returns `"categorical"` mode, the
Distinctive system returns `"scalar"` mode, and the P-base systems
return `"valued"` mode.

---

## Rendering Matrices

A `FeatureMatrix` is a data structure. To see it as a human-readable
table, pass it to `tabulate_matrix`.

### Plain text

```python
import distfeat

matrix = distfeat.minimal_matrix(["p", "b", "t", "d"])
print(distfeat.tabulate_matrix(matrix))
```

Output:

```
grapheme | alveolar | voiced
---------+----------+-------
p        | False    | False
b        | False    | True
t        | True     | False
d        | True     | True
```

### Markdown

```python
import distfeat

matrix = distfeat.minimal_matrix(["p", "b", "t", "d"])
print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

Output:

```
grapheme | alveolar | voiced
-------- | -------- | ------
p        | False    | False
b        | False    | True
t        | True     | False
d        | True     | True
```

The `format` keyword accepts `"plain"` (the default) or `"markdown"`.
The markdown variant produces a pipe table suitable for embedding in
documentation or notebooks.

### Publication-quality chart for Latin stops

The five voiceless and voiced stops of Classical Latin---/p t k b d/---
yield a three-column matrix under the default IPA system:

```python
import distfeat

matrix = distfeat.minimal_matrix(["p", "t", "k", "b", "d"])
print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

Output:

```
grapheme | alveolar | bilabial | voiced
-------- | -------- | -------- | ------
p        | False    | True     | False
t        | True     | False    | False
k        | False    | False    | False
b        | False    | True     | True
d        | True     | False    | True
```

Three features suffice. The matrix makes the structure of the inventory
immediately legible: two place features distinguish three places of
articulation (bilabial, alveolar, and velar---the last identified by the
absence of both `alveolar` and `bilabial`), while `voiced` splits the
series. The result is a five-row, three-column chart that could appear
directly in a comparative grammar.

---

## Matrices Across Systems

Different feature systems decompose the same segments into different
primitive units. Passing a `system` keyword to `minimal_matrix` reveals
these structural differences.

### Distinctive scalar mode

The Distinctive system exposes a scalar layer in which each dimension
takes the value `+1.0`, `-1.0`, or `0.0`. The minimal matrix in this
mode selects scalar dimensions rather than categorical labels:

```python
import distfeat

matrix = distfeat.minimal_matrix(
    ["p", "t", "k", "b", "d"],
    system="distinctive",
)
print(f"Mode: {matrix.mode}")
# Mode: scalar

print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

Output:

```
grapheme | anterior | dorsal | voice
-------- | -------- | ------ | -----
p        | 0.0      | 0.0    | -1.0
t        | 1.0      | 0.0    | -1.0
k        | 0.0      | 1.0    | -1.0
b        | 0.0      | 0.0    | 1.0
d        | 1.0      | 0.0    | 1.0
```

Where the IPA system needed two place columns (`alveolar`, `bilabial`),
the Distinctive system needs two as well (`anterior`, `dorsal`), but
they are continuous-valued dimensions rather than Boolean labels. The
voicing column uses `-1.0` for voiceless and `+1.0` for voiced rather
than `True`/`False`. These numerical values are what the geometry-weighted
distance algorithm operates on.

### P-base valued mode

The P-base HC system represents features as multi-state symbolic values.
Its minimal matrix uses `FeatureState` symbols (`+`, `-`, `.`) rather
than numbers or Booleans:

```python
import distfeat

matrix = distfeat.minimal_matrix(
    ["p", "t", "k", "b", "d"],
    system="pbase-hc",
)
print(f"Mode: {matrix.mode}")
# Mode: valued

print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

Output:

```
grapheme | distributed | voice
-------- | ----------- | -----
p        | +           | -
t        | -           | -
k        | .           | -
b        | +           | +
d        | -           | +
```

The P-base HC system selects `distributed` and `voice` as its minimal
pair. Notice the `.` for /k/ in the `distributed` column: the dot
symbol indicates an indeterminate value, reflecting a genuine gap in
the underlying feature specification. The P-base tradition tolerates
underspecification in a way that the categorical systems do not.

### What the comparison reveals

Three systems, three matrices, three decompositions of the same five
segments. The IPA matrix answers in Booleans, the Distinctive matrix
answers in signed scalars, and the P-base matrix answers in symbolic
feature states. None is more correct than the others; each makes
different structural commitments visible.

---

## The Geometry Tree

Feature geometry is the organizational principle that determines how
features group together and, consequently, how much weight a feature
mismatch carries when computing segment distance. `distfeat` ships a
built-in tree modeled on the Clements and Hume (1995) proposal.

### Accessing the tree

The tree is available as `DEFAULT_GEOMETRY`, a `GeometryNode` at the
root:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
print(tree.name)
# Root
```

### The five top-level branches

The root has five immediate children, each a `GeometryNode`
representing a major articulatory domain:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
for branch in tree.children:
    print(branch.name)
```

Output:

```
Laryngeal
Manner
Place
TongueRoot
Prosodic
```

**Laryngeal** covers phonation properties: voice, aspiration,
glottalization, breathy voice, and creaky voice. **Manner** covers
articulation type: sonorant, continuant, nasal, lateral, strident,
delayed release, tap, and syllabic. **Place** is the most deeply
nested branch, with five sub-nodes---Labial, Coronal, Dorsal,
Pharyngeal, and Glottal---each of which may contain further leaf
features. **TongueRoot** contains the Advanced/Retracted Tongue Root
contrast. **Prosodic** gathers suprasegmental modifications: length,
nasalization, labialization, palatalization, pharyngealization,
ejection, and stress.

### Sub-nodes under Place

The Place node illustrates the tree's depth. Its five children are
themselves `GeometryNode` objects, each containing leaf features:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
place = tree.children[2]  # Place

for sub in place.children:
    leaf_count = len(sub.children)
    leaves = ", ".join(child.name for child in sub.children)
    print(f"  {sub.name} ({leaf_count}): {leaves}")
```

Output:

```
  Labial (1): round
  Coronal (2): anterior, distributed
  Dorsal (3): high, low, back
  Pharyngeal (2): pharyngeal_place, epiglottal_place
  Glottal (1): glottal_place
```

### Leaf FeatureNode objects

At the leaves of the tree are `FeatureNode` objects. Each leaf has a
`name`, a `positive` value, and a `negative` value:

```python
import distfeat

node = distfeat.DEFAULT_GEOMETRY.find_feature("voiced")
print(node)
# FeatureNode(name='voice', positive='voiced', negative='voiceless')
```

The `positive` and `negative` strings are the feature values that
appear in categorical feature sets. When a segment's feature set
contains `"voiced"`, the `voice` node is activated in the positive
direction; when it contains `"voiceless"`, the same node is activated
in the negative direction.

The tree contains 30 leaf `FeatureNode` objects in total. Features
directly under a top-level branch (such as `voice` under Laryngeal)
sit at depth 2. Features nested under a Place sub-node (such as
`round` under Labial, or `high` under Dorsal) sit at depth 3. This
depth difference is central to the distance weighting scheme described
below.

### Tree traversal methods

`GeometryNode` provides four traversal methods for inspecting the tree:

**`all_features()`** returns every leaf positive and negative value in
the subtree as a frozenset:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
all_vals = tree.all_features()
print(len(all_vals))
# 38
print("voiced" in all_vals, "bilabial" in all_vals)
# True False
```

Note that `all_features()` collects the `positive` and `negative`
strings from `FeatureNode` objects. Values like `"bilabial"` that
appear in the `FEATURE_TO_GEOMETRY_NODE` mapping but not as leaf
`positive`/`negative` strings are not included.

**`find_feature(value)`** looks up the `FeatureNode` whose `positive`
or `negative` field matches:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
node = tree.find_feature("voiceless")
print(node.name, node.positive, node.negative)
# voice voiced voiceless
```

**`find_parent(value)`** returns the `GeometryNode` that directly
contains the matching leaf:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
parent = tree.find_parent("voiced")
print(parent.name)
# Laryngeal

parent = tree.find_parent("anterior")
print(parent.name)
# Coronal
```

**`siblings_of(value)`** returns the positive and negative values of
all *other* `FeatureNode` objects under the same parent:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY
sibs = tree.siblings_of("voiced")
print(sibs)
# frozenset({'voiceless', 'aspirated', 'glottalized', 'breathy', 'creaky'})

sibs = tree.siblings_of("anterior")
print(sibs)
# frozenset({'distributed'})
```

The Laryngeal node has five leaf children, so `"voiced"` has five
siblings (the other values in the same branch). The Coronal node has
two leaf children (`anterior` and `distributed`), so their sibling sets
are each other's values.

---

## Tree-Based Feature Relationships

The geometry tree defines a natural notion of distance between feature
values: the number of edges one must traverse to walk from one leaf to
another.

### Feature distance

The `feature_distance` method on `GeometryNode` counts tree edges
between two feature values:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY

# Same parent node (Laryngeal > voice)
d1 = tree.feature_distance("voiced", "voiceless")
print(f"voiced -- voiceless: {d1}")
# voiced -- voiceless: 2

# Different features under the same branch (Laryngeal)
d2 = tree.feature_distance("voiced", "aspirated")
print(f"voiced -- aspirated: {d2}")
# voiced -- aspirated: 4

# Different top-level branches (Laryngeal vs Manner)
d3 = tree.feature_distance("voiced", "sonorant")
print(f"voiced -- sonorant:  {d3}")
# voiced -- sonorant:  6

# Features in deeply nested sub-branches (Laryngeal vs Dorsal)
d4 = tree.feature_distance("voiced", "close")
print(f"voiced -- close:     {d4}")
# voiced -- close:     7
```

The algorithm works by computing the path from the root to each
feature value, finding the deepest common ancestor, and summing the
remaining edges. Two values under the same `FeatureNode` (like `voiced`
and `voiceless`) share a path almost all the way down, giving a
distance of 2. Two values in different top-level branches must travel
up through the root and back down, accumulating a much larger count.

### The path-distance algorithm

To understand the numbers, it helps to inspect the tree structure.
We can locate features and their parents with the public traversal
methods:

```python
import distfeat

tree = distfeat.DEFAULT_GEOMETRY

# "voiced" sits under Root > Laryngeal > voice
parent_voiced = tree.find_parent("voiced")
print(f"Parent of 'voiced': {parent_voiced.name}")
# Parent of 'voiced': Laryngeal

# "voiceless" sits under the same parent
parent_voiceless = tree.find_parent("voiceless")
print(f"Parent of 'voiceless': {parent_voiceless.name}")
# Parent of 'voiceless': Laryngeal

# "close" sits deeper: Root > Place > Dorsal > high
parent_close = tree.find_parent("close")
print(f"Parent of 'close': {parent_close.name}")
# Parent of 'close': Dorsal
```

The path from root to `voiced` is Root > Laryngeal > voice > voiced
(depth 3), and `voiceless` shares the same path up to voice.

For `voiced` vs `voiceless`, the paths share the prefix
`['Root', 'Laryngeal', 'voice']`---three common elements. The
remaining tails have length 1 each, giving a distance of 1 + 1 = 2.

For `voiced` vs `close`, the paths share only `['Root']`---one common
element. The remaining tails have lengths 3 and 4, giving 3 + 4 = 7.

The general formula is:

> distance = (len(path\_a) - common) + (len(path\_b) - common)

where *common* is the length of the shared prefix.

---

## Mapping Geometry to Romance

The geometry tree is not merely a classification device; it predicts
which sound changes should be phonologically "cheap" and which should
be "expensive." Consider two changes attested in the history of Latin
to Romance:

1. **/p/ to /b/**: voicing of a voiceless stop. This changes only the
   Laryngeal branch (voice: voiceless to voiced). Place and manner
   remain untouched.

2. **/p/ to /t/**: a change of place from bilabial to alveolar. Voicing
   and manner remain the same, but the Place branch shifts entirely.

We can verify the prediction computationally using the geometry-weighted
`sound_distance` method, which normalizes feature mismatches by their
depth in the tree:

```python
import distfeat

feats_p = distfeat.get_features("p")
feats_b = distfeat.get_features("b")
feats_t = distfeat.get_features("t")

tree = distfeat.DEFAULT_GEOMETRY

d_voice = tree.sound_distance(feats_p, feats_b)
d_place = tree.sound_distance(feats_p, feats_t)

print(f"/p/ to /b/ (voice change):  {d_voice:.4f}")
# /p/ to /b/ (voice change):  0.5455

print(f"/p/ to /t/ (place change):  {d_place:.4f}")
# /p/ to /t/ (place change):  0.1538
```

The place change (/p/ to /t/) receives a *smaller* distance than the
voice change (/p/ to /b/). This may seem counterintuitive at first, but
it reflects the geometry weighting: in the default tree, place features
sit at depth 3 (under Place > Labial or Coronal), so mismatches there
carry weight 1/3, while voice sits at depth 2 (under Laryngeal), where
mismatches carry weight 1/2. The algorithm reflects the structural
claim that laryngeal distinctions are "bigger" in the tree than
sub-place distinctions.

The full implications of this weighting become clearer when we compute
pairwise distances across the entire stop inventory. Chapter 7 takes
up that task in detail. For now, the key insight is that the geometry
tree provides a principled, theory-grounded mechanism for converting
qualitative feature differences into quantitative distances---and that
those distances can be used to model the relative likelihood of
historical sound changes.

The Romance lenition chain /p/ > /b/ > /\u03B2/ > \u2205, where a voiceless
stop progressively weakens through voicing, spirantization, and
eventual loss, involves a series of small steps in the geometry tree.
Chapter 9 will show that each individual step has a small distance,
even though the cumulative journey from /p/ to silence traverses
multiple branches. The geometry tree makes it possible to quantify this
observation precisely.

---

*Tracked examples for this chapter are collected in
`examples/ch06_matrices_and_geometry/`.*
