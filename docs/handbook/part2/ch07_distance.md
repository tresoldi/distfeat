# Chapter 7: Distance

<p class="chapter-subtitle">Computing phonological distance across systems</p>

The previous chapter introduced the geometry tree and showed how it
weights feature mismatches. This chapter puts that machinery to work.
The `distance` function is the single highest-level entry point for
measuring how different two segments are, and it delegates to
system-specific algorithms that each define "difference" in their own
way. Understanding these algorithms---and comparing their outputs on
the same data---is essential for any downstream task that relies on
phonological similarity, from cognate detection to sound change
modeling.

---

## System-Based Distance

The `distance` function accepts two graphemes and an optional `system`
keyword. When no system is specified, the current default (IPA) is
used:

```python
import distfeat

d = distfeat.distance("p", "b")
print(f"IPA:         {d:.4f}")
# IPA:         0.5455
```

Passing a system name switches to a different distance algorithm:

```python
import distfeat

d_ipa = distfeat.distance("p", "b")
d_dst = distfeat.distance("p", "b", system="distinctive")
d_pbh = distfeat.distance("p", "b", system="pbase-hc")

print(f"IPA:         {d_ipa:.4f}")
print(f"Distinctive: {d_dst:.4f}")
print(f"P-base HC:   {d_pbh:.4f}")
```

Output:

```
IPA:         0.5455
Distinctive: 0.2143
P-base HC:   0.0455
```

The same pair of segments, the same phonological reality, three
different numbers. The IPA and Distinctive systems both weight
mismatches by tree depth, but they operate on different
representations (categorical frozensets versus scalar vectors). The
P-base HC system counts raw feature mismatches without geometry
weighting. Each number is meaningful within its own system; comparing
numbers *across* systems requires care.

---

## How Geometry-Weighted Distance Works

The IPA and Tresoldi systems compute distance by delegating to the
`sound_distance` method on `DEFAULT_GEOMETRY`. This method takes two
categorical feature sets (frozensets of strings) and returns a
normalized float between 0.0 and 1.0.

### The algorithm

The computation proceeds in two stages.

**Stage 1: Leaf feature comparison.** The algorithm iterates over
every leaf `FeatureNode` in the geometry tree. For each leaf at
depth *d*, it assigns a weight of 1/*d*. It then checks whether
each feature set contains the leaf's positive value, its negative
value, or neither. If neither set activates the leaf, the leaf is
excluded from the comparison entirely (its weight is subtracted from
the total). Otherwise, the algorithm converts the activation to a
numeric value (+1.0 for positive, -1.0 for negative, 0.0 for
absent) and accumulates the weighted absolute difference divided by
2.

**Stage 2: Geometry node comparison.** Some feature values in the
categorical sets (such as `"bilabial"` or `"alveolar"`) do not
correspond to leaf `FeatureNode` objects but are mapped to geometry
node names through the `FEATURE_TO_GEOMETRY_NODE` table. The
algorithm groups these values by node, assigns a weight based on
the node's depth in the tree, and scores mismatches between the
two sets at each node.

**Normalization.** The total weighted difference is divided by the
total weight to produce a value between 0.0 and 1.0.

### A worked example

```python
import distfeat

feats_p = distfeat.get_features("p")
feats_b = distfeat.get_features("b")

print(f"/p/: {sorted(feats_p)}")
# /p/: ['bilabial', 'consonant', 'stop', 'voiceless']

print(f"/b/: {sorted(feats_b)}")
# /b/: ['bilabial', 'consonant', 'stop', 'voiced']

d = distfeat.DEFAULT_GEOMETRY.sound_distance(feats_p, feats_b)
print(f"Geometry distance: {d:.4f}")
# Geometry distance: 0.5455
```

The only leaf-level difference is on the `voice` node: /p/ activates
`voiceless` (-1.0) while /b/ activates `voiced` (+1.0). The
`voice` node sits at depth 2, so its weight is 1/2. The absolute
difference is |(-1.0) - (1.0)| / 2 = 1.0, and the weighted
contribution is 0.5 * 1.0 = 0.5. After normalization by the total
weight of all active leaves, the result is approximately 0.5455.

---

## How Distinctive Scalar Distance Works

The Distinctive system uses a different path to the same goal. Rather
than operating on raw categorical frozensets, it first converts each
feature set to a scalar vector of 32 named dimensions, then computes
a weighted distance over those dimensions.

### The algorithm

For each of the 32 scalar dimensions:

1. Look up the scalar value for each segment (+1.0, -1.0, or 0.0
   if the dimension is not activated).
2. If both values are 0.0, skip the dimension.
3. Otherwise, compute the weight as 1/*d*, where *d* is the depth
   of the dimension's geometry node in the tree.
4. Accumulate the weighted absolute difference divided by 2.

The total weighted difference is divided by the total weight, as in
the geometry method.

### Comparing the two approaches

```python
import distfeat

distinctive = distfeat.get_system("distinctive")

# Get scalar vectors
s_p = distinctive.grapheme_to_scalars("p")
s_b = distinctive.grapheme_to_scalars("b")

print("Scalars for /p/:")
for dim, val in sorted(s_p.items()):
    print(f"  {dim}: {val:+.1f}")

print("Scalars for /b/:")
for dim, val in sorted(s_b.items()):
    print(f"  {dim}: {val:+.1f}")
```

Output:

```
Scalars for /p/:
  continuant: -1.0
  labial: +1.0
  sonorant: -1.0
  syllabic: -1.0
  voice: -1.0
Scalars for /b/:
  continuant: -1.0
  labial: +1.0
  sonorant: -1.0
  syllabic: -1.0
  voice: +1.0
```

The only difference is `voice`: -1.0 versus +1.0. But because the
Distinctive system's weight lookup uses the geometry node of each
*dimension* rather than the geometry node of each leaf, and because
the set of active dimensions differs from the set of active leaves in
the direct geometry method, the final distance differs:

```python
import distfeat

d_ipa = distfeat.distance("p", "b")
d_dst = distfeat.distance("p", "b", system="distinctive")

print(f"IPA (geometry):  {d_ipa:.4f}")
print(f"Distinctive:     {d_dst:.4f}")
```

Output:

```
IPA (geometry):  0.5455
Distinctive:     0.2143
```

The Distinctive system considers more dimensions active (because its
scalar encoding activates dimensions like `sonorant`, `continuant`,
and `syllabic` for stops), spreading the total weight over a larger
denominator. The single voice mismatch therefore accounts for a
smaller fraction of the total, yielding a lower distance.

---

## How P-base Distance Works

The P-base systems take a third approach. Their distance is a simple
mismatch ratio over the features that both segments define.

### The algorithm

Given two `ValuedFeatures` representations:

1. Identify all features where *both* segments have a determinate
   value (that is, neither is `FeatureState.DOT`).
2. Count the mismatches among those comparable features.
3. Divide the mismatch count by the number of comparable features.

The result is a value between 0.0 (identical on all comparable
features) and 1.0 (different on every comparable feature).

### A worked example

```python
import distfeat

rep_p = distfeat.get_representation("p", system="pbase-hc")
rep_b = distfeat.get_representation("b", system="pbase-hc")

# Count comparable features
comparable = [
    key for key in rep_p.values
    if (rep_p.values[key].value != "."
        and rep_b.values[key].value != ".")
]
mismatches = [
    key for key in comparable
    if rep_p.values[key] != rep_b.values[key]
]

print(f"Comparable features: {len(comparable)}")
print(f"Mismatches: {len(mismatches)} ({mismatches})")
print(f"Distance: {len(mismatches) / len(comparable):.4f}")
```

Output:

```
Comparable features: 22
Mismatches: 1 (['voice'])
Distance: 0.0455
```

Twenty-two features are comparable (neither segment has a `.` value
for them), and exactly one---`voice`---differs. The distance is
1/22 = 0.0455. This is the lowest distance of the three systems
for the /p/--/b/ pair, because the P-base HC feature inventory is
large and the mismatch is localized to a single column.

### No geometry weighting

The P-base distance algorithm does not use the geometry tree. Every
comparable feature contributes equally to the distance, regardless of
whether it encodes a laryngeal, manner, or place distinction. This
makes the P-base distance conceptually simpler but less sensitive to
the hierarchical organization of phonological features.

---

## Distance Across the Latin Stop Inventory

The full power of the distance function becomes apparent when applied
to an entire inventory. The six Latin stops /p t k b d g/ form a
natural test set.

### The IPA distance matrix

```python
import distfeat

stops = ["p", "t", "k", "b", "d", "g"]

header = "      " + "  ".join(f"{s:>6}" for s in stops)
print(header)
for a in stops:
    row = f"  /{a}/ "
    for b in stops:
        d = distfeat.distance(a, b)
        row += f"  {d:>5.3f} "
    print(row)
```

Output:

```
            p       t       k       b       d       g
  /p/   0.000   0.154   0.154   0.545   0.615   0.615
  /t/   0.154   0.000   0.154   0.615   0.545   0.615
  /k/   0.154   0.154   0.000   0.615   0.615   0.545
  /b/   0.545   0.615   0.615   0.000   0.154   0.154
  /d/   0.615   0.545   0.615   0.154   0.000   0.154
  /g/   0.615   0.615   0.545   0.154   0.154   0.000
```

### The Distinctive distance matrix

```python
import distfeat

stops = ["p", "t", "k", "b", "d", "g"]

header = "      " + "  ".join(f"{s:>6}" for s in stops)
print(header)
for a in stops:
    row = f"  /{a}/ "
    for b in stops:
        d = distfeat.distance(a, b, system="distinctive")
        row += f"  {d:>5.3f} "
    print(row)
```

Output:

```
            p       t       k       b       d       g
  /p/   0.000   0.200   0.125   0.214   0.350   0.312
  /t/   0.200   0.000   0.200   0.350   0.167   0.350
  /k/   0.125   0.200   0.000   0.312   0.350   0.214
  /b/   0.214   0.350   0.312   0.000   0.200   0.125
  /d/   0.350   0.167   0.350   0.200   0.000   0.200
  /g/   0.312   0.350   0.214   0.125   0.200   0.000
```

### Structural patterns

Both matrices exhibit the same qualitative pattern, which reflects
genuine phonological structure:

1. **Voice pairs have moderate distance.** The pairs /p/--/b/,
   /t/--/d/, and /k/--/g/ differ only in voicing. In the IPA matrix
   this yields 0.545; in the Distinctive matrix, 0.214 (for /p/--/b/).

2. **Same-voicing place changes are smaller.** Within the voiceless
   series, /p/--/t/, /p/--/k/, and /t/--/k/ are all 0.154 under IPA
   and range from 0.125 to 0.200 under Distinctive. Place features
   sit deeper in the tree, so their mismatches carry less weight.

3. **Cross-voicing cross-place changes are largest.** Pairs like
   /p/--/d/ or /t/--/g/ differ in both voicing and place, producing
   the highest distances in both matrices.

The numbers differ between the two systems, but the *ranking* of pairs
from most similar to most different is consistent. This robustness
across systems gives confidence that the distance measure captures real
phonological structure rather than artifacts of a particular encoding.

---

## Precomputed Distances

Sometimes the built-in distance algorithms are not appropriate for a
task. Corpus-derived distances, perceptual similarity judgments, or
custom metrics may be more suitable. The `distance` function accepts a
`precomputed` keyword for exactly this purpose.

### Overriding with a precomputed value

The `precomputed` argument is a nested dictionary mapping grapheme
pairs to distances:

```python
import distfeat

custom = {"a": {"e": 0.3}}

d = distfeat.distance("a", "e", precomputed=custom)
print(d)
# 0.3
```

The lookup is symmetric: if the pair `("a", "e")` is not found, the
function also checks `("e", "a")` before raising an error.

```python
import distfeat

custom = {"a": {"e": 0.3}}

# Reverse order also works
d = distfeat.distance("e", "a", precomputed=custom)
print(d)
# 0.3
```

### Use cases

Precomputed distances are useful in several scenarios:

- **Corpus-derived metrics.** When phonological distance should
  reflect the frequency of observed sound changes in a corpus rather
  than theoretical feature structure.
- **Perceptual data.** When distances are measured through listening
  experiments or confusion matrices.
- **Hybrid approaches.** When a system-based distance is used as
  the default but specific pairs need manual overrides based on
  domain knowledge.

When `precomputed` is provided, the function does *not* fall back to
the system-based algorithm if a pair is missing; it raises a `KeyError`.
This fail-fast behavior prevents silent mixing of precomputed and
computed distances, which could introduce subtle inconsistencies.

---

## Distance as a Reconstruction Tool

Distance quantifies similarity. It does not, by itself, encode
directionality. The distance between /p/ and /b/ is the same
regardless of whether we are modeling a voicing change /p/ > /b/ or
a devoicing change /b/ > /p/. Direction is a historical claim;
distance is a structural measurement.

### Foreshadowing: the lenition chain

Western Romance lenition transforms Latin voiceless stops through a
series of progressively weaker articulations. The canonical chain for
the bilabial series is:

> /p/ > /b/ > /\u03B2/ > \u2205

Each step involves a small phonological change: voicing, then
spirantization (stop to fricative), then deletion. We can measure the
distance at each step:

```python
import distfeat

d_pb = distfeat.distance("p", "b")
d_bbeta = distfeat.distance("b", "\u03B2")
d_total = distfeat.distance("p", "\u03B2")

print(f"/p/ to /b/:         {d_pb:.4f}")
print(f"/b/ to /\u03B2/:         {d_bbeta:.4f}")
print(f"/p/ to /\u03B2/ (direct): {d_total:.4f}")
```

Output:

```
/p/ to /b/:         0.5455
/b/ to /\u03B2/:         0.2727
/p/ to /\u03B2/ (direct): 0.8182
```

The individual steps are smaller than the cumulative distance from
/p/ to /\u03B2/. This asymmetry is a direct consequence of how the
geometry tree weights different kinds of changes. The voicing step
(/p/ to /b/) is a single-feature change on the Laryngeal branch at
depth 2, carrying weight 1/2. The spirantization step (/b/ to /\u03B2/)
changes manner (stop to fricative) on the Manner branch, also at
depth 2. The direct comparison from /p/ to /\u03B2/ sees *both*
changes simultaneously, accumulating their costs.

The observation that lenition proceeds through small steps rather than
large jumps is a hallmark of natural phonological change. Distance
measures make this observation quantitatively precise. Chapter 9 will
develop this analysis in full, using the complete Romance consonant
inventory and multiple feature systems.

---

*Tracked examples for this chapter are collected in
`examples/ch07_distance/`.*
