# Chapter 2: From Phonemes to Bundles

<p class="chapter-subtitle">How distfeat represents phonological features</p>

The previous chapter traced the theoretical genealogy of distinctive
features from Prague structuralism to the P-base empirical tradition.
At every stage the underlying question was the same: how should we
write down what a phoneme "is"? Trubetzkoy answered in terms of
oppositions, Jakobson in terms of acoustic dimensions, Chomsky and
Halle in terms of articulatory matrices, Clements in terms of
geometric trees, and Mielke in terms of multi-system encodings.
`distfeat` inherits all of these answers and gives each one a concrete
Python data structure. This chapter surveys the three representation
types that the library supports, explains the feature category system
that makes set operations phonologically meaningful, and clarifies what
a representation is---and is not.


## 2.1 Categorical Representation

The simplest and most transparent representation in `distfeat` is the
*categorical feature bundle*: a `frozenset` of plain strings, each
string naming a feature that the segment possesses. The IPA, Tresoldi,
and Distinctive systems all produce this kind of representation.

For the Latin voiceless bilabial stop /p/, the categorical bundle is:

```
frozenset({'consonant', 'voiceless', 'bilabial', 'stop'})
```

And for the full set of Latin oral stops:

| Grapheme | Categorical features                              |
|:--------:|:-------------------------------------------------:|
| /p/      | `{'bilabial', 'consonant', 'stop', 'voiceless'}`   |
| /t/      | `{'alveolar', 'consonant', 'stop', 'voiceless'}`   |
| /k/      | `{'consonant', 'stop', 'velar', 'voiceless'}`      |
| /b/      | `{'bilabial', 'consonant', 'stop', 'voiced'}`      |
| /d/      | `{'alveolar', 'consonant', 'stop', 'voiced'}`      |
| /g/      | `{'consonant', 'stop', 'velar', 'voiced'}`         |

When `distfeat` returns such a bundle, it wraps it in a
`CategoricalFeatures` dataclass:

```
CategoricalFeatures(values=frozenset({'consonant', 'voiceless', 'bilabial', 'stop'}))
```

The `CategoricalFeatures` type is a frozen dataclass with a single
field, `values`, of type `frozenset[str]`. Frozen means the object is
immutable and hashable---it can serve as a dictionary key or set
member, and it cannot be silently mutated after creation.

The choice of frozenset is not incidental. It reflects the theoretical
claim that features within a bundle have no inherent ordering: there is
no sense in which "consonant" comes before "voiceless" in the
specification of /p/. More importantly, the standard set operations
map naturally to phonological operations:

- **Intersection** gives the shared features of two segments.
  The intersection of the feature bundles for /p/ and /b/ is
  `{'bilabial', 'consonant', 'stop'}`---exactly the features that
  define the natural class "bilabial stops."

- **Difference** gives the features that distinguish one segment from
  another. The difference between /b/ and /p/ (in the direction
  /b/ minus /p/) is `{'voiced'}`, while /p/ minus /b/ is
  `{'voiceless'}`. The voicing axis is the sole axis of contrast.

- **Union** combines feature bundles, which is useful when composing
  complex segments or applying feature-adding rules.

- **Subset testing** checks whether one bundle is a subclass of
  another. The bundle `{'consonant', 'stop'}` is a subset of the
  bundle for /p/, which confirms that /p/ belongs to the natural class
  of stops.

The feature strings themselves are drawn from a vocabulary of 94
recognized values, defined in the `FEATURE_CATEGORIES` dictionary.
These values are organized into 32 categories, the most important of
which are:

| Category        | Example values                                         |
|:----------------|:-------------------------------------------------------|
| manner          | stop, fricative, affricate, nasal, approximant, trill, tap, lateral |
| place           | bilabial, labio-dental, alveolar, post-alveolar, velar, uvular, glottal |
| height          | close, near-close, close-mid, mid, open-mid, near-open, open |
| centrality      | front, near-front, central, near-back, back            |
| roundedness     | rounded, unrounded                                     |
| phonation       | voiced, voiceless                                      |
| type            | consonant, vowel                                       |
| duration        | long, mid-long, ultra-long, ultra-short                |
| nasalization    | nasalized                                              |
| aspiration      | aspirated                                              |
| syllabicity     | syllabic, non-syllabic                                 |
| tongue_root     | advanced-tongue-root, retracted-tongue-root            |
| laminality      | apical, laminal                                        |
| stress          | primary-stress, secondary-stress                       |

The full list includes further categories for labialization,
palatalization, pharyngealization, rhotacization, velarization,
glottalization, breathiness, creakiness, ejection, rounding degree,
release type, preceding modification, relative articulation, raising,
sibilancy, voicing modification, frication, and articulation strength.
Most of these categories are relevant only for modified or secondary
segments; the core consonant and vowel inventories are captured
adequately by the first eight or nine categories.


## 2.2 Valued Representation

The four P-base systems (pbase-hc, pbase-jfh, pbase-spe, pbase-uftc)
use a different encoding. Instead of a flat set of feature names, each
segment is represented as a dictionary mapping feature names to
symbolic state values. The `ValuedFeatures` dataclass wraps this
dictionary:

```
ValuedFeatures(values={'syllabic': '-', 'vocalic': '-', 'consonantal': '+',
                       'sonorant': '-', 'continuant': '-', 'voice': '-', ...})
```

The state values are members of the `FeatureState` enumeration, a
`StrEnum` with six members:

| Symbol | Name       | Meaning                                           |
|:------:|:-----------|:--------------------------------------------------|
| `+`    | `POSITIVE` | The segment possesses this feature.                |
| `-`    | `NEGATIVE` | The segment lacks this feature.                    |
| `.`    | `DOT`      | The feature is unspecified or not applicable.       |
| `n`    | `N`        | A P-base encoding for "not applicable" or neutral. |
| `o`    | `O`        | A P-base encoding for a distinct neutral state.    |
| `x`    | `X`        | A P-base encoding for an indeterminate state.      |

The `+` and `-` values correspond directly to the SPE convention of
plus and minus. The remaining four values (`n`, `o`, `x`, `.`) are
unique to the P-base tradition and reflect the reality that not all
features are cleanly binary for all segments. When P-base encounters a
segment for which a feature is genuinely inapplicable---for example,
the feature `round` for a glottal stop---it assigns one of these
non-binary states rather than forcing a plus or minus.

To illustrate, the P-base HC encoding of /p/ looks roughly like this
(abridged for clarity):

| Feature       | State |
|:--------------|:-----:|
| syllabic      |  -    |
| vocalic       |  -    |
| consonantal   |  +    |
| sonorant      |  -    |
| continuant    |  -    |
| voice         |  -    |
| nasal         |  -    |
| strident      |  -    |
| lateral       |  n    |
| spread        |  -    |
| tense         |  .    |
| high          |  -    |
| low           |  -    |
| anterior      |  +    |
| coronal       |  -    |
| back          |  -    |
| round         |  -    |
| labial        |  +    |
| distributed   |  +    |

Note how `lateral` receives the state `n` (not applicable: laterality
is not a meaningful contrast for bilabial stops) and `tense` receives
`.` (unspecified: different sources disagree on whether /p/ is tense in
this system). These non-binary states are not noise; they carry
information about the limits of the feature system itself.

Like `CategoricalFeatures`, `ValuedFeatures` is a frozen dataclass.
Its single field, `values`, is a `dict[str, FeatureState]`. Although
dictionaries are mutable in Python, the frozen dataclass wrapper
signals the intent that the object should be treated as immutable once
created.

The `FeatureRepresentation` type alias unifies both representation
types:

```
type FeatureRepresentation = CategoricalFeatures | ValuedFeatures
```

Any function in `distfeat` that accepts or returns a "representation"
uses this type. The caller can inspect the type at runtime to determine
which encoding is in play, or use the system's `representation_kind`
property (which returns `"categorical"` or `"valued"`) to branch
without inspecting individual objects.


## 2.3 Scalar Representation

The Distinctive system occupies a middle ground. It stores features
categorically (as a frozenset, like IPA and Tresoldi), but it can also
project those features into a continuous scalar space for gradient
distance computation. Each dimension in this scalar space is a named
`ScalarDimension` object that defines:

- A **name** (e.g., `"voice"`, `"continuant"`, `"labial"`).
- A set of **positive** features that map to the value +1.0 (e.g.,
  `{"voiced"}` for the voice dimension).
- A set of **negative** features that map to the value -1.0 (e.g.,
  `{"voiceless"}` for the voice dimension).
- A **geometry node** linking the dimension to a branch of the feature
  tree (e.g., `"Laryngeal"` for voice).

The Distinctive system ships with over 30 scalar dimensions covering
the Laryngeal branch (voice, spread glottis, constricted glottis,
breathy voice, creaky voice), the Manner branch (sonorant, continuant,
nasal, lateral, strident, delayed release, tap, syllabic), the Place
branch organized by sub-node (labial, round, coronal, anterior,
distributed, dorsal, high, low, back), the TongueRoot branch (ATR),
and the Prosodic branch (long, nasalized, labialized, palatalized,
pharyngealized, ejective, rhotacized, velarized).

For /p/, the non-zero scalar values are:

| Dimension   | Value | Reason                                        |
|:------------|:-----:|:----------------------------------------------|
| voice       | -1.0  | /p/ is voiceless (maps to negative)            |
| sonorant    | -1.0  | /p/ is a consonant (maps to negative)          |
| continuant  | -1.0  | /p/ is a stop (maps to negative)               |
| syllabic    | -1.0  | /p/ is a consonant (maps to negative)          |
| labial      | +1.0  | /p/ is bilabial (maps to positive)             |

All other dimensions are zero for /p/ (neither positive nor negative
features are present), and zero-valued dimensions are omitted from the
distance computation. The resulting scalar vector is sparse: most
segments activate only a handful of the 30+ dimensions.

The distance metric in the Distinctive system works by comparing these
scalar vectors dimension by dimension, weighting each dimension
inversely by the depth of its geometry node in the feature tree.
Laryngeal dimensions, which sit at depth 2, receive a weight of 0.5;
Labial dimensions, which sit at depth 3 (under Place), receive a
weight of roughly 0.33. The effect is that laryngeal differences
(like voicing) are weighted more heavily than fine-grained place
differences (like rounding), which aligns with the typological
observation that laryngeal contrasts are perceptually more salient.

The scalar representation is not a separate representation type in the
`distfeat` data model---the Distinctive system's `get_representation`
method still returns a `CategoricalFeatures` object, just like IPA and
Tresoldi. The scalar projection is an internal mechanism used for
distance computation, accessible through the `grapheme_to_scalars` and
`features_to_scalars` methods on the `DistinctiveFeatureSystem` class
but not exposed in the top-level public API. This design keeps the
public interface uniform (every system returns either
`CategoricalFeatures` or `ValuedFeatures`) while allowing individual
systems to use richer internal representations when computing derived
quantities like distance.


## 2.4 Feature Categories as Mutual Exclusion

The `FEATURE_CATEGORIES` dictionary does more than organize features
for human readers. It encodes a constraint: features within the same
category are mutually exclusive. A segment cannot be simultaneously
`voiced` and `voiceless` (both in the `phonation` category), nor
simultaneously a `stop` and a `fricative` (both in the `manner`
category). When a phonological rule adds a feature to a segment, any
existing feature in the same category is automatically removed.

This mutual exclusion semantics is implemented in the `add_features`
operation. Consider the change from /t/ to /d/ in Latin---a simple
voicing of the alveolar stop. The feature bundle for /t/ is:

```
frozenset({'alveolar', 'consonant', 'stop', 'voiceless'})
```

Adding the feature `voiced` triggers a lookup in `FEATURE_CATEGORIES`:
`voiced` belongs to the `phonation` category. The operation then
removes any existing feature in the same category---in this case,
`voiceless`---and adds `voiced`. The result is:

```
frozenset({'alveolar', 'consonant', 'stop', 'voiced'})
```

which is exactly the feature bundle for /d/. The category system
ensures that the operation produces a well-formed bundle: no segment
ends up with contradictory feature values.

The 32 categories range from the coarse-grained (manner, place, type)
to the very specific (frication, release, preceding modification).
Some categories contain only two members (phonation: voiced/voiceless;
roundedness: rounded/unrounded; type: consonant/vowel), making them
effectively binary. Others contain many members (manner has 11 values;
place has 17), reflecting the richer space of contrasts along those
dimensions. The category system does not impose binarism; it imposes
mutual exclusion, which is a weaker but more flexible constraint.

This design supports both SPE-style fully specified segments (where
every relevant category has exactly one value present) and
underspecified segments (where some categories have no value present).
The frozenset for /p/ contains `voiceless` but could in principle omit
it entirely if the user's theory treats voicelessness as the default
for obstruents. `distfeat` does not enforce full specification; it
provides the vocabulary and the operations, and lets the user decide
how much to specify.


## 2.5 What a Representation Is Not

A design decision deserves explicit statement. `distfeat` does not
define a `Sound` class, a `Segment` class, or any object that
represents "a sound" as an entity with methods for self-modification,
phonological behavior, or acoustic rendering. The library represents
*features*, not sounds.

A `CategoricalFeatures` object is a frozen bundle of strings. A
`ValuedFeatures` object is a frozen dictionary of string-to-state
mappings. Neither carries a grapheme, a language label, a frequency
count, or an audio sample. The grapheme-to-feature mapping is held
externally by the system objects; the feature representations
themselves are anonymous bundles.

This is a deliberate choice of *data over behavior*. A frozen
dataclass with one field is the lightest possible wrapper around a
Python built-in (frozenset or dict). It is easy to serialize, easy to
compare, easy to hash, easy to pass between functions, and easy to
inspect in a debugger. It imposes no framework, no inheritance
hierarchy, no event system, and no runtime state. The trade-off is
that feature bundles know nothing about where they came from or what
they mean---they are pure data, and all interpretation is supplied
by the functions and systems that operate on them.

The `FeatureRepresentation` type alias makes this explicit:

```
type FeatureRepresentation = CategoricalFeatures | ValuedFeatures
```

There is no base class with shared methods. There is no `.distance()`
method on `CategoricalFeatures`. Distance is a function that takes
two representations and a system, not a method that lives on one
representation. This functional decomposition keeps the representation
types simple and keeps the analysis functions composable: you can pass
any pair of representations to `distance` and get a result, regardless
of how those representations were created.

For the full specification of the Latin oral stops in all three
representation styles, the following table summarizes what `distfeat`
produces:

| Grapheme | Categorical (IPA)                                | Valued (P-base HC, abridged)           | Scalar (Distinctive, non-zero only)         |
|:--------:|:------------------------------------------------:|:--------------------------------------:|:-------------------------------------------:|
| /p/      | bilabial, consonant, stop, voiceless             | consonantal=+, voice=-, labial=+, ...  | voice=-1, sonorant=-1, continuant=-1, labial=+1 |
| /t/      | alveolar, consonant, stop, voiceless             | consonantal=+, voice=-, coronal=+, ... | voice=-1, sonorant=-1, continuant=-1, coronal=+1, anterior=+1 |
| /k/      | consonant, stop, velar, voiceless                | consonantal=+, voice=-, high=+, ...    | voice=-1, sonorant=-1, continuant=-1, dorsal=+1 |
| /b/      | bilabial, consonant, stop, voiced                | consonantal=+, voice=+, labial=+, ...  | voice=+1, sonorant=-1, continuant=-1, labial=+1 |
| /d/      | alveolar, consonant, stop, voiced                | consonantal=+, voice=+, coronal=+, ... | voice=+1, sonorant=-1, continuant=-1, coronal=+1, anterior=+1 |
| /g/      | consonant, stop, velar, voiced                   | consonantal=+, voice=+, high=+, ...    | voice=+1, sonorant=-1, continuant=-1, dorsal=+1 |

Three encodings of the same six segments. Each answers a different
question: the categorical encoding tells you what descriptive labels
apply, the valued encoding tells you what theoretical features are
specified (and which are not), and the scalar encoding gives you a
vector in a continuous space where distances can be computed directly.
The next chapter shows how to retrieve these representations from the
library and begin working with them.

---

With representations defined, the reader is ready to install `distfeat`
and begin querying feature systems. Chapter 3 provides a hands-on
introduction to the library's public API.
