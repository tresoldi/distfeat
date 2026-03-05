# Chapter 4: Systems and Representations

<p class="chapter-subtitle">A tour of the seven built-in feature systems</p>

Every feature system is a particular lens through which a phoneme can be
examined. The same bilabial voiceless stop /p/ is simultaneously a
categorical bundle `{consonant, voiceless, bilabial, stop}`, a scalar
vector with `voice = -1.0` and `labial = +1.0`, and a row of SPE-style
binary values `[+anterior, -coronal, -continuant, ...]`. None of these
descriptions is more correct than the others; each foregrounds different
properties that suit different analytical tasks.

`distfeat` ships seven systems organized into four families. This chapter
introduces them one by one, shows how to access them through the
registry, and closes with a comparative table that places the eight Latin
obstruent consonants under all seven encodings at once.

---

## The Registry

Before any feature system can be queried, `distfeat` needs to know
*which* system you mean. That knowledge lives in a **registry**: a
mapping from short string names to initialized system objects.

### The lazy global registry

The simplest path is to call the module-level convenience functions. On
the very first call, `distfeat` creates a global registry populated with
all seven built-in systems and sets `"ipa"` as the default:

```python
import distfeat

# The first call triggers lazy initialization
systems = distfeat.list_systems()
print(systems)
# ['ipa', 'tresoldi', 'distinctive', 'pbase-hc', 'pbase-jfh', 'pbase-spe', 'pbase-uftc']
```

The global registry is convenient for interactive exploration. You can
change the default at any time:

```python
import distfeat

distfeat.set_default("tresoldi")

# Now bare calls resolve to Tresoldi
features = distfeat.get_features("p")
print(features)
# frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})
```

You can also register additional systems into the global registry:

```python
import distfeat

# Register a custom system under the name "my-system"
distfeat.register("my-system", my_custom_system)
```

### Explicit registries

For reproducible scripts and library code, it is better to create a
registry explicitly. The `create_registry` function accepts an optional
dataset, a flag controlling whether the seven built-in systems are
loaded, and the name of the default system:

```python
import distfeat

reg = distfeat.create_registry(
    register_builtin=True,
    default_system="distinctive",
)

print(reg.list_systems())
# ['ipa', 'tresoldi', 'distinctive', 'pbase-hc', 'pbase-jfh', 'pbase-spe', 'pbase-uftc']

sys = reg.get_system("ipa")
print(sys.name)
# 'ipa'
```

Explicit registries keep global state clean and make it easy to run
two analyses with different defaults in the same process.

### Module-level convenience functions

The following functions delegate to the global registry and are the
recommended entry point for interactive work:

| Function | Purpose |
| --- | --- |
| `list_systems()` | Return names of all registered systems |
| `get_system(name)` | Return the system object by name |
| `get_features(grapheme, *, system=None)` | Return categorical features (frozenset) |
| `get_representation(grapheme, *, system=None)` | Return the native representation |
| `register(name, system)` | Register a new system |
| `set_default(name)` | Change the default system |

When the `system` keyword is omitted, the current default is used.

---

## IPA System

The **IPA system** (`IPAFeatureSystem`) is the default. It parses the
descriptive sound name from the bundled dataset---strings like `"voiceless
bilabial stop consonant"`---and keeps only the tokens that belong to
recognized phonological categories (manner, place, phonation, height,
centrality, and so on). The result is a `frozenset[str]`.

```python
import distfeat

features = distfeat.get_features("p")
print(features)
# frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})
```

Each element in the frozenset is a human-readable label drawn from the
IPA descriptive tradition. The label set is flat: there is no internal
hierarchy, no positive/negative polarity, and no numeric value. Two
sounds are identical if and only if their feature sets are equal.

### The Latin obstruents under IPA

The eight consonants /p t k b d g f s/ form the core obstruent inventory
of Classical Latin. Under the IPA system they decompose as follows:

```python
import distfeat

latin = ["p", "t", "k", "b", "d", "g", "f", "s"]

for grapheme in latin:
    features = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(features)}")
```

Output:

```
/p/  ['bilabial', 'consonant', 'stop', 'voiceless']
/t/  ['alveolar', 'consonant', 'stop', 'voiceless']
/k/  ['consonant', 'stop', 'velar', 'voiceless']
/b/  ['bilabial', 'consonant', 'stop', 'voiced']
/d/  ['alveolar', 'consonant', 'stop', 'voiced']
/g/  ['consonant', 'stop', 'velar', 'voiced']
/f/  ['consonant', 'fricative', 'labio-dental', 'voiceless']
/s/  ['alveolar', 'consonant', 'fricative', 'sibilant', 'voiceless']
```

Notice that /s/ carries the extra label `sibilant`. This is not a
separate manner category; it is an additional articulatory property that
distinguishes /s/ from non-sibilant fricatives like /f/.

---

## Tresoldi System

The **Tresoldi system** (`TresoldiFeatureSystem`) is a broader
categorical encoding designed for cross-linguistic comparison. Like the
IPA system, it produces `frozenset[str]` bundles. The parsing strategy
differs, however: whereas the IPA system filters tokens through a fixed
category table, the Tresoldi system retains all descriptive tokens from
the sound name (except tone markers prefixed with `with_`).

```python
import distfeat

features = distfeat.get_features("p", system="tresoldi")
print(features)
# frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})
```

For the standard Latin consonants the two systems produce identical
output, because every token in the bundled sound names happens to appear
in the IPA category table as well. The difference becomes visible when
the dataset is extended with sounds whose names include descriptive
tokens outside the standard IPA category inventory. In such cases the
Tresoldi system preserves the additional labels, while the IPA system
silently drops them.

### Comparing IPA and Tresoldi

The two systems are intentionally compatible. For downstream code that
needs maximum portability across future datasets, the Tresoldi system is
the safer default. For code that relies on a well-defined category
vocabulary, the IPA system is more predictable.

```python
import distfeat

grapheme = "pʰ"

ipa_feats = distfeat.get_features(grapheme, system="ipa")
tre_feats = distfeat.get_features(grapheme, system="tresoldi")

print(f"IPA:      {sorted(ipa_feats)}")
print(f"Tresoldi: {sorted(tre_feats)}")
# IPA:      ['aspirated', 'bilabial', 'consonant', 'stop', 'voiceless']
# Tresoldi: ['aspirated', 'bilabial', 'consonant', 'stop', 'voiceless']

print(f"Sets equal: {ipa_feats == tre_feats}")
# Sets equal: True
```

---

## Distinctive System

The **Distinctive system** (`DistinctiveFeatureSystem`) occupies a middle
ground. Like the IPA and Tresoldi systems, it produces categorical
`frozenset[str]` bundles from the same underlying dataset. But it also
exposes a **scalar layer**: a dictionary mapping 32 named dimensions to
`+1.0` or `-1.0` values, following the binary feature tradition of
Chomsky and Halle (1968) updated with geometry nodes from Clements and
Hume (1995).

### Categorical features

The categorical side works identically to the IPA system:

```python
import distfeat

features = distfeat.get_features("p", system="distinctive")
print(features)
# frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})
```

### Scalar features

The scalar layer is accessible through three methods on the
`DistinctiveFeatureSystem` object. You obtain that object through
`get_system`:

```python
import distfeat

distinctive = distfeat.get_system("distinctive")
```

**`grapheme_to_scalars(grapheme)`** converts a grapheme directly to its
scalar vector:

```python
import distfeat

distinctive = distfeat.get_system("distinctive")

p_scalars = distinctive.grapheme_to_scalars("p")
print(p_scalars)
# {'voice': -1.0, 'sonorant': -1.0, 'continuant': -1.0,
#  'syllabic': -1.0, 'labial': 1.0}

b_scalars = distinctive.grapheme_to_scalars("b")
print(b_scalars)
# {'voice': 1.0, 'sonorant': -1.0, 'continuant': -1.0,
#  'syllabic': -1.0, 'labial': 1.0}
```

The only difference between /p/ and /b/ is the sign of `voice`: `-1.0`
for voiceless, `+1.0` for voiced. Dimensions that are not relevant to a
sound (neither positive nor negative) are omitted from the dictionary
rather than set to zero. This keeps the representation sparse.

**`features_to_scalars(features)`** converts a categorical frozenset to
the scalar representation:

```python
import distfeat

distinctive = distfeat.get_system("distinctive")

p_features = distfeat.get_features("p", system="distinctive")
scalars = distinctive.features_to_scalars(p_features)
print(scalars)
# {'voice': -1.0, 'sonorant': -1.0, 'continuant': -1.0,
#  'syllabic': -1.0, 'labial': 1.0}
```

**`scalars_to_features(scalars)`** converts in the opposite direction,
from scalar values back to categorical labels:

```python
import distfeat

distinctive = distfeat.get_system("distinctive")

scalars = {"voice": -1.0, "labial": 1.0, "continuant": -1.0}
features = distinctive.scalars_to_features(scalars)
print(features)
# frozenset({'voiceless', 'bilabial', 'affricate'})
```

Note that the round-trip is not always lossless. The scalar space is
lower-dimensional than the categorical space: multiple categorical labels
may map to the same scalar dimension, and a scalar value of `-1.0` on
`continuant` maps back to the first alphabetically sorted member of the
negative set (`affricate` rather than `stop`). The scalar layer is
designed for distance computation and numerical analysis, not for
faithful categorical reconstruction.

### The 32 scalar dimensions

The distinctive system defines 32 named dimensions grouped by geometry
node. The full list, ordered as they appear in the code:

| Geometry Node | Dimensions |
| --- | --- |
| Laryngeal | voice, spread\_glottis, constricted\_glottis, breathy\_voice, creaky\_voice |
| Manner | sonorant, continuant, nasal, lateral, strident, delayed\_release, tap\_feature, syllabic |
| Labial | labial, round |
| Coronal | coronal, anterior, distributed, apical |
| Dorsal | dorsal, high, low, back |
| TongueRoot | atr |
| Prosodic | long, nasalized, labialized, palatalized, pharyngealized, ejective, rhotacized, velarized |

### Scalar profiles of the Latin obstruents

```python
import distfeat

distinctive = distfeat.get_system("distinctive")

latin = ["p", "t", "k", "b", "d", "g", "f", "s"]

for grapheme in latin:
    scalars = distinctive.grapheme_to_scalars(grapheme)
    # Show only dimensions with non-zero values
    compact = {k: ("+" if v > 0 else "-") for k, v in scalars.items()}
    print(f"/{grapheme}/  {compact}")
```

Output:

```
/p/  {'voice': '-', 'sonorant': '-', 'continuant': '-', 'syllabic': '-', 'labial': '+'}
/t/  {'voice': '-', 'sonorant': '-', 'continuant': '-', 'syllabic': '-', 'coronal': '+', 'anterior': '+', 'distributed': '-'}
/k/  {'voice': '-', 'sonorant': '-', 'continuant': '-', 'syllabic': '-', 'dorsal': '+'}
/b/  {'voice': '+', 'sonorant': '-', 'continuant': '-', 'syllabic': '-', 'labial': '+'}
/d/  {'voice': '+', 'sonorant': '-', 'continuant': '-', 'syllabic': '-', 'coronal': '+', 'anterior': '+', 'distributed': '-'}
/g/  {'voice': '+', 'sonorant': '-', 'continuant': '-', 'syllabic': '-', 'dorsal': '+'}
/f/  {'voice': '-', 'sonorant': '-', 'continuant': '+', 'syllabic': '-', 'labial': '+'}
/s/  {'voice': '-', 'sonorant': '-', 'continuant': '+', 'strident': '+', 'syllabic': '-', 'coronal': '+', 'anterior': '+', 'distributed': '-'}
```

Place features are now localized to specific geometry nodes: /p/ and /f/
activate `labial`, /t/ and /s/ activate `coronal` (with `anterior` and
`distributed` sub-features), and /k/ activates `dorsal`. The scalar
representation makes these structural groupings explicit in a way that the
flat categorical set does not.

---

## P-base Systems

The **P-base family** (`PBaseFeatureSystem`) provides four systems
derived from the P-base phonological features database: `pbase-hc`,
`pbase-jfh`, `pbase-spe`, and `pbase-uftc`. Each corresponds to a
different feature theory tradition:

| System | Tradition |
| --- | --- |
| `pbase-hc` | Halle and Clements |
| `pbase-jfh` | Jakobson, Fant, and Halle |
| `pbase-spe` | Chomsky and Halle (*SPE*) |
| `pbase-uftc` | Unified Feature Theory for Consonants |

Unlike the three categorical systems above, the P-base systems return
**valued representations**: dictionaries mapping feature names to
multi-state symbolic values.

### Valued features and FeatureState

The native representation type for P-base systems is `ValuedFeatures`,
a dataclass wrapping a `dict[str, FeatureState]`. The `FeatureState`
enum defines six possible values:

| Symbol | Constant | Meaning |
| --- | --- | --- |
| `+` | `FeatureState.POSITIVE` | Feature is present / positive |
| `-` | `FeatureState.NEGATIVE` | Feature is absent / negative |
| `.` | `FeatureState.DOT` | Indeterminate (conflict or unspecified) |
| `n` | `FeatureState.N` | Not applicable |
| `o` | `FeatureState.O` | Zero / null |
| `x` | `FeatureState.X` | Variable / unspecified |

### Retrieving P-base representations

Use `get_representation` to obtain the native `ValuedFeatures` object:

```python
import distfeat

rep = distfeat.get_representation("p", system="pbase-spe")
print(type(rep))
# <class 'distfeat.representations.ValuedFeatures'>

# Inspect a few feature values
for name in ["voice", "continuant", "sonorant", "anterior", "coronal"]:
    state = rep.values[name]
    print(f"  {name}: {state.value}")
```

Output:

```
  voice: -
  continuant: -
  sonorant: -
  anterior: +
  coronal: -
```

The `get_features` function also works with P-base systems, but it
returns a flattened frozenset of `"name=value"` strings rather than a
native valued dictionary:

```python
import distfeat

features = distfeat.get_features("p", system="pbase-spe")
print(sorted(features)[:5])
# ['EXTRA=-', 'LONG=-', 'anterior=+', 'back=-', 'consonantal=+']
```

This flattened form is useful for quick inspection but loses the typed
structure. For analysis, prefer `get_representation`.

### The SPE feature vector for Latin consonants

```python
import distfeat

latin = ["p", "t", "k", "b", "d", "f", "s"]
key_features = ["voice", "continuant", "sonorant", "anterior", "coronal", "high", "back"]

header = f"{'':>4}" + "".join(f"{feat:>13}" for feat in key_features)
print(header)
print("-" * len(header))

for grapheme in latin:
    rep = distfeat.get_representation(grapheme, system="pbase-spe")
    if rep is None:
        continue
    vals = "".join(f"{rep.values[f].value:>13}" for f in key_features)
    print(f"/{grapheme}/ {vals}")
```

Output:

```
          voice    continuant     sonorant     anterior      coronal         high         back
-------------------------------------------------------------------------------------------
/p/           -             -            -            +            -            -            -
/t/           -             -            -            +            +            -            -
/k/           -             -            -            -            -            +            +
/b/           +             -            -            +            -            -            -
/d/           +             -            -            +            +            -            -
/f/           -             +            -            +            -            -            -
/s/           -             +            -            +            +            -            -
```

Notice that /g/ is absent from the P-base SPE table. The P-base dataset
uses the IPA symbol U+0261 (LATIN SMALL LETTER SCRIPT G) for the voiced
velar stop, not the ASCII `g`. This is a common encoding divergence in
phonological databases. When working across systems, always verify that
the grapheme encoding matches the database convention.

### Duplicate-merging policy

Some graphemes appear more than once in the P-base source data. When the
system encounters duplicates, it applies a conservative merge:

- **Identical duplicates** collapse silently.
- **Conflicting values** for the same feature are resolved to
  `FeatureState.DOT` (`.`), signaling indeterminacy.

This policy avoids silently choosing one value over another while
preserving as much information as possible.

---

## Comparing Systems on Romance Data

The table below shows the eight Latin obstruents under all seven systems.
For the three categorical systems, features are shown as a sorted list.
For the four P-base systems, a compact `+/-/./n` notation is used for a
selected subset of features.

### Categorical systems (IPA, Tresoldi, Distinctive)

For the basic Latin obstruents, the three categorical systems produce
identical feature sets:

| Grapheme | Features |
| --- | --- |
| /p/ | bilabial, consonant, stop, voiceless |
| /t/ | alveolar, consonant, stop, voiceless |
| /k/ | consonant, stop, velar, voiceless |
| /b/ | bilabial, consonant, stop, voiced |
| /d/ | alveolar, consonant, stop, voiced |
| /g/ | consonant, stop, velar, voiced |
| /f/ | consonant, fricative, labio-dental, voiceless |
| /s/ | alveolar, consonant, fricative, sibilant, voiceless |

The three systems diverge on sounds with richer descriptive names---sounds
carrying tone markers, secondary articulations, or phonation modifiers
that lie outside the core IPA category vocabulary. The IPA system
filters strictly; the Tresoldi system retains more; the Distinctive
system adds the scalar layer.

### Distinctive system --- scalar view

The same eight consonants in the scalar representation show a different
kind of structure:

| Grapheme | voice | sonorant | continuant | labial | coronal | dorsal | strident |
| --- | --- | --- | --- | --- | --- | --- | --- |
| /p/ | - | - | - | + | | | |
| /t/ | - | - | - | | + | | |
| /k/ | - | - | - | | | + | |
| /b/ | + | - | - | + | | | |
| /d/ | + | - | - | | + | | |
| /g/ | + | - | - | | | + | |
| /f/ | - | - | + | + | | | |
| /s/ | - | - | + | | + | | + |

Empty cells indicate that the dimension is not activated for that
segment. The table makes the voicing contrast (first column), the
manner contrast (continuant), and the three-way place split (labial /
coronal / dorsal) immediately visible.

### P-base SPE --- valued view (selected features)

| Grapheme | voice | continuant | sonorant | anterior | coronal | high | back |
| --- | --- | --- | --- | --- | --- | --- | --- |
| /p/ | - | - | - | + | - | - | - |
| /t/ | - | - | - | + | + | - | - |
| /k/ | - | - | - | - | - | + | + |
| /b/ | + | - | - | + | - | - | - |
| /d/ | + | - | - | + | + | - | - |
| /f/ | - | + | - | + | - | - | - |
| /s/ | - | + | - | + | + | - | - |

The SPE system encodes place differently from the Distinctive system.
Where the Distinctive system uses three independent nodes (labial,
coronal, dorsal), the SPE system uses a combination of `anterior`,
`coronal`, `high`, and `back`. The velar stop /k/, for instance, is
`[+high, +back]` in SPE but simply `[+dorsal]` in the Distinctive
system. These are not contradictions; they are different theoretical
decompositions of the same articulatory reality.

### What the comparison reveals

The same eight phonemes, viewed through seven systems, yield three
distinct types of insight:

1. **Categorical systems** answer membership questions: *Is /p/ a stop?
   Is it voiceless?* They are ideal for natural-class queries and
   rule-based manipulation.

2. **The scalar layer** answers gradient questions: *How different are /p/
   and /b/?* It supports distance computation and numerical clustering.

3. **Valued systems** answer theory-specific questions: *What is the SPE
   specification for /k/?* They preserve the full detail of a particular
   feature framework.

Choosing the right system depends on the task. The next chapter shows
how to use feature queries to assemble natural classes and manipulate
segment inventories.

---

*Tracked examples for this chapter are collected in
`examples/ch04_systems_and_representations/`.*
