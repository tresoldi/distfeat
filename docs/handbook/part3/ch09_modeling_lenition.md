# Chapter 9: Modeling Western Romance Lenition

Chapter 8 assembled the raw material: consonant inventories,
feature bundles, and comparative reflex sets for five Romance
daughters of Latin.  This chapter puts the material to work.
Western Romance lenition---the weakening of intervocalic stops
through voicing, spirantization, and deletion---is one of the
best-documented diachronic processes in comparative linguistics.
We model it here as a trajectory through feature space, measure
the distance traversed at each stage, and compare the profiles
that different feature systems produce.

The chapter is the synthesis toward which the handbook has been
building.  It draws on every module introduced in Part II:
feature lookup (Chapter 4), natural-class queries (Chapter 5),
geometry and matrices (Chapter 6), and distance (Chapter 7).

---

## The Lenition Chain

The traditional account of Western Romance lenition describes a
three-stage chain that applies to voiceless stops between vowels:

> Stage 0 (Latin): voiceless stop
> Stage 1: voiced stop (voicing)
> Stage 2: voiced fricative (spirantization)
> Stage 3: zero (deletion)

The chain applies in parallel across the three places of articulation:

| Stage | Labial | Coronal | Dorsal |
|-------|--------|---------|--------|
| 0     | /p/    | /t/     | /k/    |
| 1     | /b/    | /d/     | /g/    |
| 2     | /β/    | /ð/     | /ɣ/    |
| 3     | zero   | zero    | zero   |

Not every daughter language has completed every stage.  Italian and
Romanian remain at Stage 0 (retention of voiceless stops in most
environments).  Spanish and Portuguese reach Stage 1 in the
phonemic system, with allophonic spirantization to Stage 2.  French
has gone the furthest, reaching Stage 3 in many etyma.  The chain
is thus a comparative gradient, not a single event.

We can verify the feature bundles at each stage with distfeat:

```python
import distfeat

chains = {
    "Labial":  ["p", "b", "β"],
    "Coronal": ["t", "d", "ð"],
    "Dorsal":  ["k", "g", "ɣ"],
}

for series, segments in chains.items():
    print(f"--- {series} ---")
    for grapheme in segments:
        feats = distfeat.get_features(grapheme)
        print(f"  /{grapheme}/  {sorted(feats)}")
    print()
```

```
--- Labial ---
  /p/  ['bilabial', 'consonant', 'stop', 'voiceless']
  /b/  ['bilabial', 'consonant', 'stop', 'voiced']
  /β/  ['bilabial', 'consonant', 'fricative', 'voiced']

--- Coronal ---
  /t/  ['alveolar', 'consonant', 'stop', 'voiceless']
  /d/  ['alveolar', 'consonant', 'stop', 'voiced']
  /ð/  ['consonant', 'dental', 'fricative', 'voiced']

--- Dorsal ---
  /k/  ['consonant', 'stop', 'velar', 'voiceless']
  /g/  ['consonant', 'stop', 'velar', 'voiced']
  /ɣ/  ['consonant', 'fricative', 'velar', 'voiced']
```

The labial and dorsal series are perfectly parallel: at each stage the
same feature changes apply and the place feature is preserved.  The
coronal series shows a minor complication: /t/ and /d/ are `alveolar`,
but /ð/ is `dental`.  This reflects the phonetic reality that the
dental fricative [ð] is articulated slightly further forward than the
alveolar stop [d].  The discrepancy will affect the distance
calculations below, and it is worth keeping in mind as a reminder
that feature databases encode phonetic descriptions, not abstract
phonological categories.

---

## Feature Distance at Each Stage

The `distance` function computes the geometry-weighted distance
between two segments in the default IPA system.  We compute three
values for each series: Stage 0 to 1 (voicing), Stage 1 to 2
(spirantization), and the cumulative distance from Stage 0 to 2.

```python
import distfeat

chains = {
    "Labial":  ("p", "b", "β"),
    "Coronal": ("t", "d", "ð"),
    "Dorsal":  ("k", "g", "ɣ"),
}

print(f"{'Series':<10} {'0->1':>8} {'1->2':>8} {'0->2':>8}")
print("-" * 38)

for series, (s0, s1, s2) in chains.items():
    d01 = distfeat.distance(s0, s1)
    d12 = distfeat.distance(s1, s2)
    d02 = distfeat.distance(s0, s2)
    print(f"{series:<10} {d01:>8.4f} {d12:>8.4f} {d02:>8.4f}")
```

```
Series       0->1     1->2     0->2
--------------------------------------
Labial     0.5455   0.2727   0.8182
Coronal    0.5455   0.4545   1.0000
Dorsal     0.5455   0.2727   0.8182
```

Several patterns emerge.  First, Stage 0 to 1 (voicing) has the same
distance across all three series: 0.5455.  This makes sense---voicing
is a single laryngeal flip, and the geometry tree assigns the same
weight to that flip regardless of place.  Second, Stage 1 to 2
(spirantization) is smaller for labials and dorsals (0.2727) than for
coronals (0.4545).  The larger coronal distance reflects the
place shift from `alveolar` to `dental` noted above: /d/ and /ð/
differ not only in manner but also in sub-place specification, so
the distance is greater.  Third, the cumulative distance from
Stage 0 to 2 is not the sum of the two per-stage distances.  It is
computed directly from the full feature difference between /p/ and
/β/ (or /t/ and /ð/, etc.), and the geometry weighting means that
the cumulative measure is slightly less than the sum of the parts.
This reflects the nonlinear structure of the feature space: distance
is not simply additive.

---

## Geometry-Weighted Analysis

The distance values above are computed by the geometry tree
(`DEFAULT_GEOMETRY`), which assigns higher weight to features that
sit closer to the root.  We can inspect which tree dimensions carry
each stage of lenition.

### Stage 0 to 1: the Laryngeal node

Voicing flips a single feature under the Laryngeal node.  We can
measure the tree distance between the two feature values:

```python
import distfeat

d = distfeat.feature_distance("voiced", "voiceless")
print(f"feature_distance('voiced', 'voiceless') = {d}")
```

```
feature_distance('voiced', 'voiceless') = 2.0
```

The tree distance of 2 (one edge from `voiced` to the `voice`
FeatureNode, one edge from there to `voiceless`) confirms that
this is a minimal opposition within the Laryngeal subtree.  The
Laryngeal node sits at depth 2 in the geometry (directly under the
Root), so its weight is 1/2 = 0.5---high enough to make voicing
a prominent contributor to segment distance.

### Stage 1 to 2: the Manner node

Spirantization changes the manner from stop to fricative.  In
distfeat's geometry, the `continuant` feature (whose positive value
is `continuant` and whose negative value is the absence of the
feature) sits under the Manner node at depth 2.  The Manner node
itself is a direct child of the Root, so manner features also carry
a weight of 1/2.

We can verify this by examining the sound distance function
directly, passing in constructed feature sets:

```python
import distfeat

# /b/ features
b_feats = distfeat.get_features("b")
# /β/ features
beta_feats = distfeat.get_features("β")

d = distfeat.sound_distance(b_feats, beta_feats)
print(f"sound_distance(b, β) = {d:.4f}")

# The difference: stop is replaced by fricative
print(f"  /b/ manner:  stop     (in {sorted(b_feats)})")
print(f"  /β/ manner:  fricative (in {sorted(beta_feats)})")
```

```
sound_distance(b, β) = 0.2727
  /b/ manner:  stop     (in ['bilabial', 'consonant', 'stop', 'voiced'])
  /β/ manner:  fricative (in ['bilabial', 'consonant', 'fricative', 'voiced'])
```

The distance 0.2727 is less than the voicing distance (0.5455)
because the manner change (stop to fricative) is mediated through
the geometry node's grouping of manner features, and the normalized
calculation distributes the weight across all relevant dimensions.

---

## The Lenition Matrix

The `minimal_matrix` function finds the smallest set of features
that distinguishes a group of segments.  Applied to the lenition
chain, it reveals the phonological apparatus of the process.

```python
import distfeat

# Two-stage matrix: voicing only
mat_voice = distfeat.minimal_matrix(["p", "b"])
print("Voicing opposition:")
print(distfeat.tabulate_matrix(mat_voice))
print()

# Three-stage matrix: voicing + spirantization
mat_lenition = distfeat.minimal_matrix(["p", "b", "β"])
print("Lenition chain (labial):")
print(distfeat.tabulate_matrix(mat_lenition))
```

```
Voicing opposition:
grapheme | voiced
---------+-------
p        | False
b        | True

Lenition chain (labial):
grapheme | fricative | voiced
---------+-----------+-------
p        | False     | False
b        | False     | True
β        | True      | True
```

For the two-segment set {/p/, /b/}, a single feature suffices:
`voiced`.  When we add /β/ to the set, the matrix needs a second
column, `fricative`, to separate /β/ from /b/.  The matrix has
identified the two features that together encode the entire
lenition trajectory: voicing and continuancy.

This is the formal correlate of the traditional description.
Lenition in Western Romance is a process that manipulates exactly
two phonological dimensions: laryngeal specification (voiced vs.
voiceless) and manner specification (stop vs. fricative).  Place
plays no role---the matrix does not include `bilabial`, `alveolar`,
or `velar`---because place is invariant across the stages.  The
`minimal_matrix` captures this automatically.

---

## Distinctive Scalar Perspective

The `distinctive` system provides scalar representations of
segments: each phonological dimension receives a value of +1.0,
-1.0, or 0.0 (unspecified).  This gives us a different lens on the
lenition chain.

```python
import distfeat

sys = distfeat.get_system("distinctive")

print(f"{'grapheme':<10} {'voice':>7} {'contin':>7} {'labial':>7} {'sonor':>7} {'syllab':>7}")
print("-" * 48)

for grapheme in ["p", "b", "β"]:
    sc = sys.grapheme_to_scalars(grapheme)
    print(
        f"/{grapheme}/"
        f"{sc.get('voice', 0):>9.1f}"
        f"{sc.get('continuant', 0):>7.1f}"
        f"{sc.get('labial', 0):>7.1f}"
        f"{sc.get('sonorant', 0):>7.1f}"
        f"{sc.get('syllabic', 0):>7.1f}"
    )
```

```
grapheme     voice  contin  labial  sonor  syllab
------------------------------------------------
/p/         -1.0   -1.0    1.0   -1.0   -1.0
/b/          1.0   -1.0    1.0   -1.0   -1.0
/β/          1.0    1.0    1.0   -1.0   -1.0
```

The scalar trajectory is now visible as a sequence of sign flips.
Stage 1 (voicing) flips `voice` from -1.0 to +1.0.  Stage 2
(spirantization) flips `continuant` from -1.0 to +1.0.  All other
dimensions remain constant.  The chain is a walk through a
five-dimensional hypercube in which exactly one coordinate flips
at each step.

We can track the same pattern for the coronal and dorsal series:

```python
import distfeat

sys = distfeat.get_system("distinctive")

for label, segments in [("Coronal", ["t","d","ð"]), ("Dorsal", ["k","g","ɣ"])]:
    print(f"--- {label} ---")
    for grapheme in segments:
        sc = sys.grapheme_to_scalars(grapheme)
        print(f"  /{grapheme}/  voice={sc.get('voice',0):+.0f}  continuant={sc.get('continuant',0):+.0f}")
    print()
```

```
--- Coronal ---
  /t/  voice=-1  continuant=-1
  /d/  voice=+1  continuant=-1
  /ð/  voice=+1  continuant=+1

--- Dorsal ---
  /k/  voice=-1  continuant=-1
  /g/  voice=+1  continuant=-1
  /ɣ/  voice=+1  continuant=+1
```

All three series show the same scalar trajectory: voice flips first,
then continuant flips.  The scalar representation makes the structural
parallelism of lenition across places of articulation especially
transparent.

The `distinctive` system also computes its own distance metric,
weighted by the geometry.  Comparing it with the default IPA
distances:

```python
import distfeat

chains = {
    "Labial":  ("p", "b", "β"),
    "Coronal": ("t", "d", "ð"),
    "Dorsal":  ("k", "g", "ɣ"),
}

print(f"{'':15} {'IPA 0->1':>10} {'IPA 1->2':>10} {'DST 0->1':>10} {'DST 1->2':>10}")
print("-" * 58)

for series, (s0, s1, s2) in chains.items():
    d01_ipa = distfeat.distance(s0, s1)
    d12_ipa = distfeat.distance(s1, s2)
    d01_dst = distfeat.distance(s0, s1, system="distinctive")
    d12_dst = distfeat.distance(s1, s2, system="distinctive")
    print(f"{series:<15} {d01_ipa:>10.4f} {d12_ipa:>10.4f} {d01_dst:>10.4f} {d12_dst:>10.4f}")
```

```
                  IPA 0->1   IPA 1->2   DST 0->1   DST 1->2
----------------------------------------------------------
Labial            0.5455     0.2727     0.2143     0.2143
Coronal           0.5455     0.4545     0.1667     0.2222
Dorsal            0.5455     0.2727     0.2143     0.2143
```

In the distinctive system, voicing and spirantization produce
nearly equal distances for labials and dorsals (both 0.2143).
The IPA system, by contrast, assigns voicing a much higher
distance (0.5455) than spirantization (0.2727).  This is because
the two systems group features differently: the IPA system treats
`stop` and `fricative` as categorically distinct manner values
within the geometry, while the distinctive system treats them as
endpoints of the `continuant` scalar dimension.  The choice of
system shapes the distance profile of the same phonological process.

---

## Cross-System Comparison

We can push the comparison further by bringing in the P-base SPE
system, which encodes segments using the classical Chomsky and Halle
(1968) feature framework with multi-valued features:

```python
import distfeat

chains = {
    "Labial":  ("p", "b", "β"),
    "Coronal": ("t", "d", "ð"),
}

print(f"{'':15} {'IPA':>8} {'distinct':>10} {'pbase-spe':>10}")
print("-" * 45)

for series, (s0, s1, s2) in chains.items():
    d_ipa = distfeat.distance(s0, s2)
    d_dst = distfeat.distance(s0, s2, system="distinctive")
    d_spe = distfeat.distance(s0, s2, system="pbase-spe")
    print(f"{series} (0->2)  {d_ipa:>8.4f} {d_dst:>10.4f} {d_spe:>10.4f}")
```

```
                    IPA   distinct  pbase-spe
---------------------------------------------
Labial (0->2)    0.8182     0.4286     0.1250
Coronal (0->2)   1.0000     0.3889     0.1304
```

The absolute magnitudes differ dramatically.  The IPA system produces
the largest distances because it operates on a small feature set where
each feature carries high weight.  The P-base SPE system produces the
smallest distances because it distributes information across 25
dimensions, and each individual flip carries proportionally less
weight.  The distinctive system falls in between.

Despite the differences in magnitude, all three systems agree on
the qualitative structure: the cumulative distance from Stage 0 to
Stage 2 is greater than either per-stage distance, and the labial
and coronal series produce comparable (though not identical)
trajectories.  The systems differ in *how much* distance they assign,
not in *where* they assign it.  This is a useful finding for
computational historical linguistics: the relative ranking of
segment pairs by distance is more stable across feature systems
than the absolute distance values.

---

## Asymmetry and Directionality

All distance functions in distfeat are symmetric:

```python
import distfeat

d_forward  = distfeat.distance("p", "b")
d_backward = distfeat.distance("b", "p")
print(f"distance('p', 'b') = {d_forward:.4f}")
print(f"distance('b', 'p') = {d_backward:.4f}")
print(f"Symmetric: {d_forward == d_backward}")
```

```
distance('p', 'b') = 0.5455
distance('b', 'p') = 0.5455
Symmetric: True
```

Yet lenition is directional.  In the history of the Romance
languages, /p/ weakens to /b/ between vowels, but /b/ does not
strengthen to /p/ in that environment.  Fortition---the reverse
of lenition---does occur in natural languages, but it is rarer and
operates under different conditions.  The lenition chain is a
one-way street.

This asymmetry is a property of the phonological *process*, not of
the feature *space*.  The distance between /p/ and /b/ measures how
different the two segments are; it says nothing about which direction
of change is more likely.  Directionality requires information that
lies outside the feature representation: phonetic substance (the
aerodynamic conditions that favor voicing between vowels),
prosodic context (intervocalic position), and historical evidence
(the comparative method).  distfeat provides the first ingredient
---a measure of structural similarity---but not the second or third.

This is not a limitation to apologize for; it is a principled design
boundary.  A distance metric is a measuring instrument, not a theory
of change.  The comparative method uses distances to group languages
and identify correspondences, but the inference of directionality
rests on external evidence: which stage is older (established by
text attestation), which stage is cross-linguistically more common
as an input (established by typological surveys), and which stage
is phonetically more natural as a predecessor (established by
laboratory phonetics).  distfeat can quantify the *result* of
lenition but not its *cause*.

---

## From Feature Distance to Reconstruction

We can now map the five daughter languages onto the lenition
chain and measure each one's distance from the Latin ancestor.

### Stage assignments

| Language   | Stage | Intervocalic reflex of /p/ | Distance from Latin /p/ |
|------------|-------|----------------------------|------------------------|
| Italian    | 0     | /p/ (retained)             | 0.0000                 |
| Romanian   | 0     | /p/ (retained)             | 0.0000                 |
| Spanish    | 1     | /b/ (voiced)               | 0.5455                 |
| Portuguese | 1     | /b/ (voiced)               | 0.5455                 |
| French     | 3     | zero (deleted)             | --                     |

```python
import distfeat

# Distance from Latin /p/ to each attested reflex
for label, reflex in [("Italian", "p"), ("Romanian", "p"),
                       ("Spanish", "b"), ("Portuguese", "b")]:
    d = distfeat.distance("p", reflex)
    print(f"{label:<12} /p/ -> /{reflex}/  distance = {d:.4f}")
```

```
Italian      /p/ -> /p/  distance = 0.0000
Romanian     /p/ -> /p/  distance = 0.0000
Spanish      /p/ -> /b/  distance = 0.5455
Portuguese   /p/ -> /b/  distance = 0.5455
```

French is absent from this table because the reflex is zero, and
distfeat cannot compute a distance to a segment that does not exist.
But the pattern among the surviving reflexes is clear: the
conservative languages (Italian, Romanian) show zero distance from
the Latin form, while the innovative languages (Spanish, Portuguese)
show a uniform distance of 0.5455.

### The lenition isogloss

This distance pattern maps directly onto the traditional lenition
isogloss that divides Western Romance (Spanish, Portuguese, French)
from the more conservative varieties (Italian, Romanian).  The
isogloss marks the boundary between languages that underwent
intervocalic voicing and those that did not.  distfeat's distance
metric encodes the same division numerically: zero distance on one
side of the isogloss, non-zero distance on the other.

The quantitative encoding has a practical advantage: it
generalizes.  The traditional isogloss is a binary classification
(voicing or no voicing), but the distance metric places languages
on a continuous scale.  If we had a language that underwent partial
voicing---voicing of /p/ and /k/ but not /t/, for instance---its
average distance from Latin would fall between the Italian value
(0.0) and the Spanish value (0.5455).  The metric can capture
gradient variation that a binary isogloss cannot.

### The comparative method, quantified

The comparative method works by identifying systematic
correspondences between languages and reconstructing the ancestor
that best explains the pattern.  The lenition data illustrate
this process in miniature.  The correspondences are:

- Italian /p/ : Spanish /b/ : Portuguese /b/ : Romanian /p/

The reconstruction is Latin */p/, the segment that minimizes total
distance to the attested reflexes (Italian and Romanian contribute
0, Spanish and Portuguese contribute 0.5455 each).  Reconstructing
*/b/ would produce higher total distance (Italian and Romanian would
each contribute 0.5455, and Spanish and Portuguese would contribute
0).  The sum is the same, but the tie is broken by external evidence
(Italian and Romanian are more conservative) and by the typological
generalization that voiceless stops are more frequent in the world's
languages than voiced stops, making */p/ a more plausible
proto-segment.

distfeat does not perform reconstruction automatically.  But it
provides the distance measures that a reconstruction algorithm
would use as input.  The feature space encodes the comparative
method's intuition---that correspondence sets cluster around a
prototype---in a form that is computable and reproducible.

---

## Conclusions

This chapter has modeled Western Romance lenition as a trajectory
through feature space.  The key findings are:

**What distfeat shows.**  Lenition is a two-dimensional process:
voicing (Laryngeal node) followed by spirantization (Manner node).
The minimal matrix identifies these two dimensions automatically.
The distance metric assigns a quantitative profile to each stage,
and the scalar representation in the distinctive system makes the
trajectory visible as a sequence of sign flips.  Different feature
systems agree on the qualitative structure of lenition but differ in
the absolute distances they assign.

**What distfeat does not show.**  The directionality of lenition
(why /p/ weakens to /b/ and not the reverse), the conditioning
environment (why lenition applies between vowels), and the
phonetic mechanism (aerodynamic voicing, reduction of articulatory
effort).  These questions require evidence and theory beyond the
reach of a feature distance metric.

**The gap between description and explanation.**  distfeat describes
the structure of sound change: it identifies the features that
distinguish input from output and measures the distance between them.
But description is not explanation.  The feature distance between
/p/ and /b/ tells us *what changed* and *how much*, but not *why*.
Phonological theory, phonetic experimentation, and historical
attestation supply the explanatory layer.  distfeat is one instrument
among many, and its value lies precisely in the precision of its
measurements---measurements that would be subjective or
impressionistic without a formal feature space to anchor them.

The Romance consonant thread that has run through this handbook
began in Chapter 1 with the observation that phonologists carve
the continuous space of speech sounds into discrete categories.
It ends here with the observation that those categories, once
formalized as feature bundles, impose a measurable geometry on
the space of possible changes.  Lenition is not a mysterious drift;
it is a walk through a well-defined feature space, and distfeat
gives us the coordinates.

---

*Reference implementation: `examples/ch09_modeling_lenition/`*
