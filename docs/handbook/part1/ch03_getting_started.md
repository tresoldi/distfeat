# Chapter 3: Getting Started with distfeat

<p class="chapter-subtitle">Installation, first lookups, and basic operations</p>

The first two chapters developed the theoretical and representational
ground. This chapter puts the library in the reader's hands. By its
end you will have installed `distfeat`, looked up features for the
Latin stops, compared representations across systems, queried sound
classes, and computed your first segment distances.


## 3.1 Installation

`distfeat` is distributed as a pure-Python package with zero runtime
dependencies. Install it from PyPI:

```bash
pip install distfeat
```

For development work---running tests, building docs, linting---install
with the optional development extras:

```bash
pip install -e ".[dev]"
```

Verify that the installation succeeded and check the version:

```python
import distfeat

print(distfeat.__version__)
# 0.4.0
```

`distfeat` requires Python 3.12 or newer. If the import fails, check
your Python version with `python3 --version`.


## 3.2 First Lookup

The most common operation is retrieving the feature set for a given
IPA grapheme. The `get_features` function takes a grapheme string and
returns a frozenset of feature names, or `None` if the grapheme is
unknown.

```python
import distfeat

# Look up the Latin voiceless stops
p_feats = distfeat.get_features("p")
t_feats = distfeat.get_features("t")
k_feats = distfeat.get_features("k")

print(sorted(p_feats))
# ['bilabial', 'consonant', 'stop', 'voiceless']

print(sorted(t_feats))
# ['alveolar', 'consonant', 'stop', 'voiceless']

print(sorted(k_feats))
# ['consonant', 'stop', 'velar', 'voiceless']
```

The three voiceless stops share `consonant`, `stop`, and `voiceless`;
they differ in place (bilabial, alveolar, velar). Now the voiced
counterparts:

```python
b_feats = distfeat.get_features("b")
d_feats = distfeat.get_features("d")

print(sorted(b_feats))
# ['bilabial', 'consonant', 'stop', 'voiced']

print(sorted(d_feats))
# ['alveolar', 'consonant', 'stop', 'voiced']
```

The difference between /p/ and /b/ is exactly one feature: `voiceless`
vs `voiced`. Everything else is shared. This is the frozenset
representation from Chapter 2 in action.

By default, `get_features` uses the IPA system. You can request a
different system with the `system` keyword argument:

```python
# Tresoldi features for /p/
p_tresoldi = distfeat.get_features("p", system="tresoldi")
print(sorted(p_tresoldi))
# ['bilabial', 'consonant', 'stop', 'voiceless']
```

For the IPA and Tresoldi systems, the core consonant features are
identical. Differences emerge for modified segments and vowels, as
Chapter 4 will explore.


## 3.3 Representations

While `get_features` returns a plain frozenset, `get_representation`
returns the full typed representation object: a `CategoricalFeatures`
for categorical systems, or a `ValuedFeatures` for P-base systems.

```python
import distfeat

# Categorical representation (default IPA system)
rep_ipa = distfeat.get_representation("p")
print(rep_ipa)
# CategoricalFeatures(values=frozenset({'voiceless', 'consonant', 'bilabial', 'stop'}))

print(type(rep_ipa).__name__)
# CategoricalFeatures
```

Now compare with a P-base system:

```python
# Valued representation (P-base HC system)
rep_hc = distfeat.get_representation("p", system="pbase-hc")
print(type(rep_hc).__name__)
# ValuedFeatures

# Inspect the feature-state dictionary
for name, state in sorted(rep_hc.values.items()):
    print(f"  {name:15s} {state.value}")
```

The output will show each feature mapped to one of the symbolic states
(`+`, `-`, `.`, `n`). Notice that P-base HC uses feature names like
`consonantal`, `sonorant`, and `labial` (theoretical features from the
Halle & Clements tradition) rather than descriptive labels like
`consonant`, `stop`, and `bilabial` (the IPA naming convention). The
two encodings capture the same phonological reality in different
vocabularies.

The `FeatureRepresentation` type alias unifies both kinds:

```python
from distfeat import CategoricalFeatures, ValuedFeatures

# You can check which kind you have
if isinstance(rep_ipa, CategoricalFeatures):
    print("Categorical:", sorted(rep_ipa.values))

if isinstance(rep_hc, ValuedFeatures):
    print("Valued:", len(rep_hc.values), "features")
```


## 3.4 Systems

The library ships seven built-in feature systems. List them with
`list_systems`:

```python
import distfeat

systems = distfeat.list_systems()
print(systems)
# ['ipa', 'tresoldi', 'distinctive', 'pbase-hc', 'pbase-jfh', 'pbase-spe', 'pbase-uftc']
```

The first three (ipa, tresoldi, distinctive) are categorical systems
that return `CategoricalFeatures`. The last four (pbase-hc, pbase-jfh,
pbase-spe, pbase-uftc) are valued systems that return
`ValuedFeatures`.

To see how the same segment looks across systems, compare /p/:

```python
import distfeat

for name in distfeat.list_systems():
    feats = distfeat.get_features("p", system=name)
    if feats is not None:
        preview = sorted(feats)[:5]  # first 5 for brevity
        print(f"  {name:15s} {preview}{'...' if len(feats) > 5 else ''}")
```

Categorical systems return descriptive labels like `bilabial` and
`stop`. P-base systems return encoded strings like `consonantal=+`
and `voice=-`. Both are valid feature specifications of the same
segment; the difference is in the naming convention and the
underlying theoretical framework.

You can also retrieve a system object directly with `get_system`:

```python
ipa = distfeat.get_system("ipa")
print(ipa.name)
# ipa

print(ipa.representation_kind)
# categorical
```


## 3.5 Sound Classes

Sound classes are named groups of segments that share a defining set of
features. `distfeat` ships approximately 20 predefined classes, using
uppercase letter symbols following a convention common in historical
linguistics. The `is_class` function checks whether a symbol is a
known class, and `get_class_features` returns its defining features.

```python
import distfeat

# Is "S" a sound class?
print(distfeat.is_class("S"))
# True

# What features define the stop class?
s_feats = distfeat.get_class_features("S")
print(sorted(s_feats))
# ['stop']
```

The class `S` is defined by the single feature `stop`---any segment
whose feature bundle includes `stop` is a member of this class.

Other commonly used classes include:

```python
# C = consonants, V = vowels, N = nasal consonants, F = fricatives
for cls in ["C", "V", "N", "F", "L", "K", "P", "R"]:
    if distfeat.is_class(cls):
        feats = distfeat.get_class_features(cls)
        print(f"  {cls}: {sorted(feats)}")
```

The full set of predefined classes is:

| Class | Description               | Defining features              |
|:-----:|:--------------------------|:-------------------------------|
| A     | Affricates                | affricate                      |
| B     | Back vowels               | back, vowel                    |
| C     | Consonants                | consonant                      |
| CV    | Voiced consonants         | consonant, voiced              |
| E     | Front vowels              | front, vowel                   |
| F     | Fricatives                | fricative                      |
| H     | Glottal segments          | glottal                        |
| K     | Velar segments            | velar                          |
| L     | Laterals                  | lateral                        |
| N     | Nasal consonants          | consonant, nasal               |
| P     | Bilabial segments         | bilabial                       |
| Q     | Uvular segments           | uvular                         |
| R     | Non-stop consonants       | -stop, consonant               |
| S     | Stops                     | stop                           |
| SV    | Voiced stops              | stop, voiced                   |
| SVL   | Voiceless stops           | stop, voiceless                |
| V     | Vowels                    | vowel                          |
| VL    | Long vowels               | long, vowel                    |
| VN    | Nasalized vowels          | nasalized, vowel               |

Note that class `R` uses a negative feature (`-stop`) to define
"non-stop consonants"---segments that are consonants but not stops,
which captures the sonorant and fricative consonants. The minus prefix
means "must not have this feature."


## 3.6 Distance

The `distance` function computes a normalized distance between two
segments, using the feature geometry to weight the contribution of
each differing feature. The result is a float between 0.0 (identical)
and 1.0 (maximally different).

```python
import distfeat

# Voicing pair: /p/ vs /b/
d_pb = distfeat.distance("p", "b")
print(f"distance(p, b) = {d_pb:.4f}")
# distance(p, b) = 0.5455

# Place pair: /p/ vs /t/
d_pt = distfeat.distance("p", "t")
print(f"distance(p, t) = {d_pt:.4f}")
# distance(p, t) = 0.1538

# Manner + place change: /p/ vs /s/
d_ps = distfeat.distance("p", "s")
print(f"distance(p, s) = {d_ps:.4f}")
# distance(p, s) = 0.4062
```

The results confirm the geometry-based prediction from Chapter 1:
changing place within the same manner class (/p/ to /t/) produces a
smaller distance than changing both manner and place (/p/ to /s/).
The voicing contrast (/p/ to /b/) falls between the two because
the Laryngeal node sits at a relatively shallow depth in the geometry
tree, giving voicing differences a high weight.

You can specify a different system for the distance computation:

```python
# Distance using the distinctive system
d_pb_dist = distfeat.distance("p", "b", system="distinctive")
d_pt_dist = distfeat.distance("p", "t", system="distinctive")
print(f"distinctive distance(p, b) = {d_pb_dist:.4f}")
print(f"distinctive distance(p, t) = {d_pt_dist:.4f}")
```

Different systems may produce different absolute distance values, but
the relative ordering---which pairs are closer and which are
farther---generally agrees across systems for well-established
contrasts. Chapter 7 will examine the distance metric in detail and
explain exactly how the geometry weighting works.

---

The complete scripts for this chapter are available in the
`examples/ch03_getting_started/` directory.

{{ include_example("ch03_getting_started/run.py") }}

{{ example_output("ch03_getting_started") }}
