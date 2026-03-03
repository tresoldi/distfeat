# Chapter 1: Features as Theory

<p class="chapter-subtitle">An intellectual genealogy of distinctive features</p>

Phonological features did not begin as a convenience for software
engineers. They began as a claim about the architecture of human
language: that the minimal units of phonological contrast are not
whole segments but sub-segmental properties---binary or scalar axes
along which sounds oppose one another. Before writing a single line of
code it is worth understanding where this claim came from, what forms
it has taken, and why it matters for computational work today. This
chapter traces the genealogy from Prague structuralism through
generative phonology to geometrical models and large-scale empirical
databases, arriving at last at the question that `distfeat` is
designed to answer: how do we make these theoretical objects available
to programs?


## 1.1 The Prague Inheritance

The story begins with Nikolai Trubetzkoy's *Grundzuge der Phonologie*,
published posthumously in 1939. Trubetzkoy's central insight was that
phonology is not about sounds as physical events but about sounds as
members of an *opposition system*. Two sounds are distinct phonemes in
a language if and only if they stand in a relationship of opposition:
substituting one for the other changes the meaning of at least one
word. The phoneme /p/ in Latin is not simply "a voiceless bilabial
stop"; it is the term that contrasts with /b/ along the axis of
voicing, with /t/ along the axis of place, and with /f/ along the axis
of manner. The features *are* the axes.

Trubetzkoy classified oppositions in several ways---bilateral versus
multilateral, proportional versus isolated, privative versus
equipollent---but it was the privative opposition that proved most
consequential. In a privative opposition one member possesses a
"mark" that the other lacks. Latin /b/ possesses voicing; Latin /p/
lacks it. This asymmetry laid the groundwork for the idea that
features are binary: each segment either has the property or does not.

Roman Jakobson, working first with Trubetzkoy in Prague and later with
Gunnar Fant and Morris Halle at MIT, took the Prague framework in a
more universalist direction. The *Preliminaries to Speech Analysis*
(Jakobson, Fant & Halle 1952) proposed that the entire phonological
space of all human languages could be spanned by a small set of
acoustic-perceptual feature dimensions: grave/acute,
compact/diffuse, tense/lax, and so on. Each dimension was defined in
terms of measurable acoustic correlates, and every phoneme in every
language could in principle be specified as a bundle of plus and minus
values on these dimensions.

Two commitments from this early work survive in `distfeat` and in
most modern feature systems:

1. **Features as axes of contrast, not descriptions.** A feature is
   not a label attached after the fact; it is a dimension along which
   phonemes oppose one another. When `distfeat` returns the feature
   set `{'consonant', 'voiceless', 'bilabial', 'stop'}` for /p/, those
   four strings are not a prose description of how to pronounce the
   sound. They are the coordinates that locate /p/ in the contrastive
   space relative to /b/ (which differs in voicing), to /t/ (which
   differs in place), and to /f/ (which differs in manner).

2. **Universality.** The feature inventory is meant to apply across
   languages. The same dimension that opposes /p/ and /b/ in Latin
   opposes /p/ and /b/ in Mandarin, even if the two languages differ
   in what other voicing contrasts they exploit. This is why `distfeat`
   ships a single feature space shared across all its systems rather
   than language-specific inventories.


## 1.2 The Generative Turn

Chomsky and Halle's *The Sound Pattern of English* (SPE, 1968) recast
features as the primitive vocabulary of phonological rules. Where
Jakobson had grounded features in acoustic correlates, SPE shifted the
grounding to articulation. The feature `[+voice]` was defined not by
a spectral property but by the state of the glottis during production;
`[+anterior]` referred to the location of a constriction relative to
the alveolar ridge. The feature set was also significantly expanded:
SPE proposed roughly two dozen features to handle the full inventory
of English, with the understanding that the same features would extend
to all languages.

The key formal innovation of SPE was the *feature matrix*. Every
morpheme in the lexicon was stored as a matrix of segments, and every
segment was a column of plus and minus feature values. Phonological
rules operated on this matrix by changing values---flipping a minus to
a plus, or spreading a value from one column to the next. The Latin
voiceless bilabial stop /t/, for example, would receive roughly the
following SPE specification:

| Feature        | Value |
|:---------------|:-----:|
| consonantal    |   +   |
| sonorant       |   -   |
| continuant     |   -   |
| voice          |   -   |
| nasal          |   -   |
| lateral        |   -   |
| anterior       |   +   |
| coronal        |   +   |
| strident       |   -   |
| distributed    |   -   |
| high           |   -   |
| low            |   -   |
| back           |   -   |
| round          |   -   |

(The exact inventory of features varied across versions of SPE and
subsequent revisions; the table above is representative rather than
definitive.)

SPE established several conventions that persist today:

- **Binary values.** Every feature takes the value + or -, never a
  third state. This strict binarism was later relaxed by some
  theories (and by P-base, as we will see below), but the plus/minus
  notation remains the standard idiom.

- **Full specification.** Every segment is specified for every
  feature, even when the value is predictable. An alternative
  approach---underspecification theory---leaves predictable values
  blank, filling them in by rule. `distfeat` supports both approaches:
  categorical systems are fully specified, while valued systems (P-base)
  use the dot symbol `.` for unspecified features.

- **Natural classes.** A set of segments that share a feature value
  forms a natural class. "Voiceless stops" is the set of segments that
  are `[+consonantal, -sonorant, -continuant, -voice]`. Rules that
  affect voiceless stops need not list them individually; they target
  the class by its feature description. This concept of natural
  classes underpins the `is_class` and `get_class_features` functions
  in `distfeat`.


## 1.3 Feature Geometry

By the mid-1980s it had become clear that features are not all created
equal. Some features behave as a unit in phonological processes: the
laryngeal features (voicing, aspiration, glottalization) spread
together in many languages, while the place features (labial, coronal,
dorsal) form another cohesive group. George N. Clements proposed in
1985 that features are organized in a hierarchical tree, with internal
nodes grouping related features and a root node dominating everything.
Clements and Elizabeth Hume refined this model in 1995 into what is now
known as *feature geometry*.

The geometry adopted by `distfeat` (exposed as `DEFAULT_GEOMETRY`)
follows the Clements & Hume tradition and has five major branches
beneath the root:

```
Root
 +-- Laryngeal
 |    +-- voice (voiced / voiceless)
 |    +-- spread_glottis (aspirated)
 |    +-- constricted_glottis (glottalized)
 |    +-- breathy_voice (breathy)
 |    +-- creaky_voice (creaky)
 +-- Manner
 |    +-- sonorant (sonorant / obstruent)
 |    +-- continuant (continuant)
 |    +-- nasal
 |    +-- lateral
 |    +-- strident (sibilant)
 |    +-- delayed_release (affricate)
 |    +-- tap_feature (tap)
 |    +-- syllabic (syllabic / non-syllabic)
 +-- Place
 |    +-- Labial
 |    |    +-- round (rounded / unrounded)
 |    +-- Coronal
 |    |    +-- anterior
 |    |    +-- distributed
 |    +-- Dorsal
 |    |    +-- high (close / open)
 |    |    +-- low (near-open / near-close)
 |    |    +-- back (back / front)
 |    +-- Pharyngeal
 |    |    +-- pharyngeal_place
 |    |    +-- epiglottal_place
 |    +-- Glottal
 |         +-- glottal_place
 +-- TongueRoot
 |    +-- atr (advanced-tongue-root / retracted-tongue-root)
 +-- Prosodic
      +-- long, nasalized, labialized, palatalized,
          pharyngealized, ejective, primary-stress
```

The tree structure makes a prediction: features that are close in the
tree should pattern together more often than features that are far
apart. Changing /p/ to /b/ requires moving only within the Laryngeal
subtree (flipping `voiceless` to `voiced`), while changing /p/ to /s/
requires changes in both the Manner subtree (from stop to fricative,
adding sibilant and continuant) and the Place subtree (from Labial to
Coronal). The tree predicts that the first change is "smaller" than
the second, and this prediction aligns with typological
evidence: /p/ to /b/ voicing alternations are far more common
cross-linguistically than /p/ to /s/ alternations.

This insight is directly operationalized in `distfeat`. The
`DEFAULT_GEOMETRY` tree assigns each feature a depth, and the distance
metric weights feature differences inversely by depth: features deeper
in the tree (more specific) contribute less to overall distance than
features nearer the root (more general). When you call
`distance("p", "b")`, the library computes a geometry-weighted distance
that is smaller than `distance("p", "s")`, precisely because the
features that differ between /p/ and /b/ all sit within a single
shallow subtree, while the features that differ between /p/ and /s/
span multiple subtrees at different levels.

Feature geometry thus provides the conceptual bridge between the
qualitative intuition that "voicing is a small change" and the
quantitative distance metric that `distfeat` computes. Chapter 7 will
explore the distance computation in detail; for now, the key point is
that the tree is not a decorative metaphor but a structural commitment
with measurable consequences.


## 1.4 The Empirical Turn

By the end of the twentieth century, phonological theory had produced
not one feature system but several---each grounded in different
assumptions about what the primitive features are and how they map to
articulatory or acoustic properties. Jeff Mielke's *P-base* project
(first described in Mielke 2008) confronted this plurality head-on
by assembling phonological inventories and rule patterns from hundreds
of languages and encoding each segment in multiple feature systems
simultaneously.

P-base organizes its feature systems into four families:

- **HC** --- the Halle & Clements tradition, rooted in the feature
  geometry approach.
- **JFH** --- the Jakobson, Fant & Halle acoustic tradition.
- **SPE** --- the Chomsky & Halle articulatory tradition from *The
  Sound Pattern of English*.
- **UFTC** --- a "unified feature theory for the characterization"
  approach that attempts to reconcile the others.

Each family encodes the same phonological reality using different
feature labels and different structural assumptions. The segment /p/
in HC might be specified as `[+consonantal, -sonorant, -continuant,
-voice, +labial, +anterior]`, while in SPE the same segment gets a
partially overlapping but not identical set of feature names and
values. Each encoding is internally consistent, but none is
uniquely "correct" in any absolute sense.

This empirical plurality is the historical reason that `distfeat` ships
seven built-in systems rather than one. Three of those systems---IPA,
Tresoldi, and Distinctive---are categorical systems developed within
the library's own tradition, encoding features as frozensets of
descriptive labels. The remaining four---pbase-hc, pbase-jfh,
pbase-spe, and pbase-uftc---are the P-base families, encoding features
as dictionaries of multi-state values (the symbols `+`, `-`, `.`, `n`,
`o`, `x`). By exposing all seven systems through a single protocol, the
library lets the user choose the encoding that best fits their
research question without committing the software to a single
theoretical camp.

P-base also introduced a pragmatic lesson: there is no master list of
features that everyone agrees on, and any software that pretends
otherwise will eventually frustrate its users. `distfeat` takes this
lesson seriously by making its system registry extensible: users can
register new systems at runtime, built from custom datasets or
alternative theoretical frameworks.


## 1.5 Features in Computation

Computational phonology needs features in machine-readable form for
the same reason that computational chemistry needs atomic weights in
machine-readable form: because the theory provides the primitives that
algorithms operate on. Sound correspondences across languages are
stated in terms of features; phonological distance metrics are
computed over feature vectors; natural language processing systems that
handle pronunciation data need to know which sounds are "similar" and
which are "different". In every case, the feature system is not the
object of study but the instrument that makes study possible.

Yet the relationship between theory and instrument is not trivial.
Different feature systems can yield different distance rankings,
different natural class memberships, and different predictions about
which sound changes are likely. A researcher who uses SPE features
is implicitly adopting a different model of phonological space from
one who uses Jakobson-Fant-Halle features, and the two models may
disagree about whether a particular pair of sounds is "close" or
"far." Making this implicit choice explicit---and making it easy to
switch between alternatives---is the core design goal of `distfeat`.

The library is therefore best understood not as an implementation of a
particular phonological theory but as a *toolkit* that implements
several theories in a common format. It does not adjudicate between
SPE and feature geometry; it gives both a place at the table and
provides the machinery---lookup, distance, natural classes,
matrices---to use either one (or any user-defined system) as input to
downstream computation.

This stance has a practical consequence for the reader of this
handbook. When we show that `distance("p", "b")` returns a certain
number, that number is not a fact about phonology; it is a measurement
taken with a particular instrument (the default IPA system with
geometry-weighted distance). Switching the system parameter may change
the number. The handbook will always be explicit about which system is
in use, and Chapter 4 will compare the systems in detail so that the
reader can make an informed choice.

---

With the theoretical ground prepared, the next chapter turns from
abstract features to concrete data representations: how `distfeat`
encodes the bundles, valued dictionaries, and scalar vectors that make
features computable.
