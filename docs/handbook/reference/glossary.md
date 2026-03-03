# Glossary

Cross-domain definitions bridging phonology, computation, and distfeat
terminology.

---

## A

**add_features**
:   A distfeat function that adds features to a feature set with
    category-aware replacement. If the added feature belongs to the same
    category (e.g., phonation) as an existing feature, the old feature is
    removed.

**affricate**
:   A manner of articulation that begins as a stop and releases into a
    fricative. In distfeat, the feature value `"affricate"` in the Manner
    geometry node.

**alveolar**
:   A place of articulation at the alveolar ridge. Mapped to the Coronal
    geometry node.

**ATR (Advanced Tongue Root)**
:   A tongue-root articulation where the root is pushed forward, expanding
    the pharyngeal cavity. Encoded as `"advanced-tongue-root"` in the
    TongueRoot geometry node.

---

## B

**bilabial**
:   A place of articulation using both lips. Mapped to the Labial geometry
    node.

**binary feature**
:   A feature that takes two values: positive (`+`) and negative (`-`).
    The SPE tradition (Chomsky & Halle 1968) systematically uses binary
    features.

---

## C

**categorical feature**
:   A feature expressed as a label without a value scale. In distfeat,
    categorical features are stored in `CategoricalFeatures` as a
    `frozenset[str]`.

**CategoricalFeatures**
:   A frozen dataclass in distfeat wrapping `frozenset[str]`. The native
    representation for IPA, Tresoldi, and Distinctive systems.

**Clements & Hume (1995)**
:   The feature geometry model implemented in distfeat's `DEFAULT_GEOMETRY`.
    Organizes features into a hierarchical tree: Laryngeal, Manner, Place,
    TongueRoot, Prosodic.

**continuant**
:   A manner feature for segments produced with a continuous airflow (no
    complete closure). Fricatives and approximants are [+continuant]; stops
    are [-continuant].

---

## D

**daughter language**
:   A language descended from a common ancestor (proto-language). In this
    handbook, Italian, Spanish, French, Portuguese, and Romanian are daughter
    languages of Latin.

**DEFAULT_GEOMETRY**
:   The pre-built `GeometryNode` tree in distfeat encoding the Clements &
    Hume (1995) feature geometry.

**derive_class_features**
:   A distfeat function that computes the intersection of features shared by
    all graphemes in a set: the natural class they define.

**distance**
:   A distfeat function returning a normalized `float` between 0.0
    (identical) and 1.0 (maximally different) for two graphemes.

**distinctive feature**
:   A phonological property that distinguishes one phoneme from another
    within a language's inventory. The term originates with the Prague School
    (Jakobson, Fant & Halle 1952).

**DistinctiveFeatureSystem**
:   A distfeat system that extends categorical features with a scalar layer.
    Provides `grapheme_to_scalars`, `features_to_scalars`, and
    `scalars_to_features`.

---

## F

**feature bundle**
:   The set of distinctive features that specifies a phoneme. In distfeat,
    a feature bundle is a `frozenset[str]` or a `dict[str, FeatureState]`.

**feature category**
:   A mutually exclusive group of feature values (e.g., `manner` includes
    `stop`, `fricative`, `nasal`, etc.). Defined in `FEATURE_CATEGORIES`.

**feature geometry**
:   A hierarchical organization of features reflecting their phonological
    grouping. Used in distfeat for distance weighting.

**FeatureDataset**
:   A frozen dataclass holding the three TSV tables (sounds, classes,
    features) that drive a distfeat registry.

**FeatureMatrix**
:   A frozen dataclass representing a minimal set of features that uniquely
    distinguishes a set of graphemes.

**FeatureNode**
:   A leaf node in the geometry tree. Has a `name`, `positive` value, and
    optionally a `negative` value.

**FeatureRepresentation**
:   Type alias: `CategoricalFeatures | ValuedFeatures`.

**FeatureState**
:   A `StrEnum` with values `+`, `-`, `.`, `n`, `o`, `x`. Used by P-base
    valued systems.

**FeatureSystem**
:   The structural protocol that all distfeat systems implement. Any
    conforming object can be registered and used interchangeably.

**fricative**
:   A manner of articulation with turbulent airflow through a narrow
    constriction. E.g., /f/, /s/, /x/.

**frozenset**
:   A Python immutable set type. Used in distfeat for categorical feature
    bundles because features have no inherent order and set operations
    (union, intersection, difference) map naturally to phonological
    operations.

---

## G

**geometry-weighted distance**
:   The distance algorithm used by categorical systems. Iterates over
    geometry tree leaves, weighting mismatches by 1/depth so that deeper
    (more specific) features contribute less.

**GeometryNode**
:   An internal node in the feature geometry tree. Has a `name` and
    `children` (which may be other `GeometryNode`s or `FeatureNode`s).

**grapheme**
:   A written symbol representing a speech sound. In distfeat, graphemes
    are IPA symbols (e.g., `"p"`, `"b"`, `"ʃ"`).

---

## I

**IPAFeatureSystem**
:   The default distfeat system. Derives categorical features from the NAME
    field of the sound dataset (e.g., "voiceless bilabial stop" for /p/).

**IPA (International Phonetic Alphabet)**
:   A standardized system of phonetic notation. distfeat uses IPA symbols
    as grapheme identifiers.

---

## J

**Jakobson, Fant & Halle (1952)**
:   Authors of *Preliminaries to Speech Analysis*, which established the
    distinctive feature framework. The JFH feature family is one of the four
    P-base systems in distfeat.

---

## L

**Laryngeal**
:   A top-level node in the Clements & Hume geometry tree. Contains voice,
    spread glottis, constricted glottis, breathy voice, and creaky voice.

**lenition**
:   A weakening process in which consonants lose articulatory strength.
    Typical chain: voiceless stop → voiced stop → fricative → approximant →
    deletion. The central case study of this handbook.

---

## M

**Manner**
:   A top-level geometry node containing features related to the mode of
    airflow: sonorant, continuant, nasal, lateral, strident, delayed release,
    tap, syllabic.

**minimal matrix**
:   The smallest set of features that uniquely identifies each segment in a
    given set. Computed by `minimal_matrix`.

---

## N

**natural class**
:   A group of segments sharing a feature bundle that no segment outside the
    group shares. In distfeat, `derive_class_features` computes the shared
    features of a natural class.

**normalization (grapheme)**
:   distfeat applies NFD Unicode normalization and IPA equivalence mapping
    (e.g., U+0261 ɡ → g) to input graphemes.

---

## P

**P-base**
:   A database of phonological feature systems compiled by Mielke (2008).
    distfeat includes four P-base families: HC, JFH, SPE, UFTC.

**PBaseFeatureSystem**
:   A distfeat system for P-base feature families. Returns `ValuedFeatures`
    with `FeatureState` values. Instantiated with a `family` parameter.

**partial_match**
:   A distfeat function that checks whether a pattern (feature set) is a
    subset of a target, supporting negative features prefixed with `"-"`.

**phoneme**
:   An abstract sound unit that distinguishes meaning in a language. In
    distfeat, phonemes are represented by their feature bundles, not as
    objects.

**Place**
:   A top-level geometry node with sub-nodes: Labial, Coronal, Dorsal,
    Pharyngeal, Glottal.

**Prague School**
:   The linguistic tradition (Trubetzkoy, Jakobson) that originated
    distinctive feature theory in the 1930s.

**privative feature**
:   A feature that is either present or absent, with no explicit negative
    pole. In the geometry tree, privative features have an empty `negative`
    field.

**Prosodic**
:   A top-level geometry node for suprasegmental and secondary features:
    length, nasalization, labialization, palatalization, pharyngealization,
    ejection, stress.

**protocol (structural typing)**
:   A Python typing mechanism where conformance is checked by method
    signatures, not inheritance. `FeatureSystem` is a protocol.

---

## R

**reflex**
:   The outcome of a sound in a daughter language. E.g., Latin /p/ has the
    reflex /p/ in Italian but /b/ in intervocalic Spanish.

**Registry**
:   A mutable container of named `FeatureSystem` instances. distfeat
    maintains a lazy global registry and supports explicit isolated
    registries.

---

## S

**scalar dimension**
:   A continuous axis (+1.0 to -1.0) in the Distinctive system. Each
    dimension corresponds to a geometry node and is used for gradient
    distance computation.

**sound class**
:   A predefined grouping of graphemes by shared features. Identified by
    uppercase symbols (e.g., `"S"` for stops, `"V"` for vowels). Checked
    with `is_class`.

**sound_distance**
:   A distfeat function computing the normalized distance between two
    categorical feature sets using geometry weighting.

**SPE (The Sound Pattern of English)**
:   Chomsky & Halle (1968). The foundational generative phonology work that
    established universal binary features. The SPE feature family is one of
    the four P-base systems.

---

## T

**TongueRoot**
:   A top-level geometry node containing the ATR (advanced tongue root)
    feature.

**Tresoldi system**
:   A categorical feature system with broader descriptive labels than the
    IPA system. Named after the author of distfeat.

**TresoldiFeatureSystem**
:   The distfeat class implementing the Tresoldi categorical system.

---

## V

**valued feature**
:   A feature with an explicit symbolic value from `FeatureState` (e.g.,
    `+`, `-`, `.`). Used by P-base systems.

**ValuedFeatures**
:   A frozen dataclass wrapping `dict[str, FeatureState]`. The native
    representation for P-base systems.
