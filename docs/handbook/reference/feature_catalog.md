# Feature Catalog

This page catalogs the feature values, categories, and geometry tree
available in distfeat.

---

## Feature Categories

Features in distfeat are organized into mutually exclusive categories. When
features are composed via `add_features`, a new feature replaces any existing
feature in the same category. The `FEATURE_CATEGORIES` dictionary maps each
feature value to its category name.

### Type

| Feature | Description |
|---------|-------------|
| `consonant` | Consonantal segment |
| `vowel` | Vocalic segment |

### Phonation

| Feature | Description |
|---------|-------------|
| `voiced` | Vocal fold vibration present |
| `voiceless` | Vocal fold vibration absent |

### Manner

| Feature | Description |
|---------|-------------|
| `stop` | Complete oral closure |
| `fricative` | Turbulent airflow through narrow constriction |
| `affricate` | Stop release into fricative |
| `nasal` | Nasal airflow |
| `approximant` | Open approximation without turbulence |
| `trill` | Repeated vibration of articulator |
| `tap` | Single brief closure |
| `lateral` | Airflow around tongue sides |
| `click` | Ingressive velaric airstream |
| `implosive` | Ingressive glottalic airstream |
| `nasal-click` | Click with nasal release |
| `plosive` | Alias for `stop` |

### Place

| Feature | Description |
|---------|-------------|
| `bilabial` | Both lips |
| `labio-dental` | Lower lip and upper teeth |
| `labio-velar` | Lips and velum simultaneously |
| `labio-palatal` | Lips and palate simultaneously |
| `dental` | Tongue tip/blade and upper teeth |
| `alveolar` | Tongue tip/blade and alveolar ridge |
| `post-alveolar` | Behind the alveolar ridge |
| `alveolo-palatal` | Between alveolar and palatal |
| `retroflex` | Tongue tip curled back |
| `palatal` | Tongue body and hard palate |
| `palatal-velar` | Between palatal and velar |
| `velar` | Tongue body and velum |
| `uvular` | Tongue body and uvula |
| `pharyngeal` | Tongue root and pharynx |
| `epiglottal` | Epiglottis |
| `glottal` | Glottis |
| `linguolabial` | Tongue tip and upper lip |
| `labial` | General labial articulation |

### Height (vowels)

| Feature | Description |
|---------|-------------|
| `close` | Highest tongue position |
| `near-close` | Between close and close-mid |
| `close-mid` | Upper-mid tongue position |
| `mid` | Central tongue height |
| `open-mid` | Lower-mid tongue position |
| `near-open` | Between open-mid and open |
| `open` | Lowest tongue position |

### Centrality (vowels)

| Feature | Description |
|---------|-------------|
| `front` | Tongue advanced |
| `near-front` | Between front and central |
| `central` | Neither front nor back |
| `near-back` | Between central and back |
| `back` | Tongue retracted |

### Roundedness

| Feature | Description |
|---------|-------------|
| `rounded` | Lip rounding present |
| `unrounded` | Lip rounding absent |

### Duration

| Feature | Description |
|---------|-------------|
| `long` | Extended duration |
| `mid-long` | Intermediate duration |
| `ultra-long` | Exceptionally extended |
| `ultra-short` | Exceptionally brief |

### Secondary Articulations

| Category | Features |
|----------|----------|
| Nasalization | `nasalized` |
| Labialization | `labialized` |
| Palatalization | `palatalized`, `labio-palatalized` |
| Velarization | `velarized` |
| Pharyngealization | `pharyngealized` |
| Aspiration | `aspirated` |
| Glottalization | `glottalized` |
| Breathiness | `breathy` |
| Creakiness | `creaky` |
| Ejection | `ejective` |
| Rhotacization | `rhotacized` |

### Syllabicity

| Feature | Description |
|---------|-------------|
| `syllabic` | Functions as syllable nucleus |
| `non-syllabic` | Does not function as nucleus |

### Sibilancy

| Feature | Description |
|---------|-------------|
| `sibilant` | High-frequency turbulence |

### Voicing modifications

| Feature | Description |
|---------|-------------|
| `devoiced` | Partially devoiced |
| `revoiced` | Re-voiced after devoicing |

### Relative articulation

| Feature | Description |
|---------|-------------|
| `advanced` | Articulator moved forward |
| `retracted` | Articulator moved back |
| `centralized` | Moved toward central position |
| `mid-centralized` | Moved toward mid-central |

### Raising

| Feature | Description |
|---------|-------------|
| `raised` | Articulator raised |
| `lowered` | Articulator lowered |

### Articulation

| Feature | Description |
|---------|-------------|
| `strong` | Fortis articulation |

### Release

| Feature | Description |
|---------|-------------|
| `unreleased` | No audible release |
| `with-lateral-release` | Released laterally |
| `with-nasal-release` | Released nasally |
| `with-mid-central-vowel-release` | Released with schwa |

### Frication

| Feature | Description |
|---------|-------------|
| `with-frication` | Accompanied by friction noise |

### Tongue root

| Feature | Description |
|---------|-------------|
| `advanced-tongue-root` | Tongue root advanced (ATR) |
| `retracted-tongue-root` | Tongue root retracted (RTR) |

### Laminality

| Feature | Description |
|---------|-------------|
| `apical` | Tongue tip as articulator |
| `laminal` | Tongue blade as articulator |

### Preceding modifications

| Feature | Description |
|---------|-------------|
| `pre-aspirated` | Aspiration before closure |
| `pre-glottalized` | Glottalization before closure |
| `pre-labialized` | Labialization before closure |
| `pre-nasalized` | Nasalization before closure |
| `pre-palatalized` | Palatalization before closure |

### Stress

| Feature | Description |
|---------|-------------|
| `primary-stress` | Primary lexical stress |
| `secondary-stress` | Secondary lexical stress |

### Tone

Features for tonal specification: `with_downstep`, `with_extra-high_tone`,
`with_extra-low_tone`, `with_falling_tone`, `with_global_fall`,
`with_global_rise`, `with_high_tone`, `with_low_tone`, `with_mid_tone`,
`with_rising_tone`, `with_upstep`.

---

## Feature Geometry Tree

The `DEFAULT_GEOMETRY` constant encodes the Clements & Hume (1995)
feature geometry. The tree has five top-level branches under a `Root` node.

```
Root
├── Laryngeal
│   ├── voice: voiced / voiceless
│   ├── spread_glottis: aspirated
│   ├── constricted_glottis: glottalized
│   ├── breathy_voice: breathy
│   └── creaky_voice: creaky
├── Manner
│   ├── sonorant: sonorant / obstruent
│   ├── continuant: continuant
│   ├── nasal: nasal
│   ├── lateral: lateral
│   ├── strident: sibilant
│   ├── delayed_release: affricate
│   ├── tap_feature: tap
│   └── syllabic: syllabic / non-syllabic
├── Place
│   ├── Labial
│   │   └── round: rounded / unrounded
│   ├── Coronal
│   │   ├── anterior: anterior
│   │   └── distributed: distributed
│   ├── Dorsal
│   │   ├── high: close / open
│   │   ├── low: near-open / near-close
│   │   └── back: back / front
│   ├── Pharyngeal
│   │   ├── pharyngeal_place: pharyngeal
│   │   └── epiglottal_place: epiglottal
│   └── Glottal
│       └── glottal_place: glottal
├── TongueRoot
│   └── atr: advanced-tongue-root / retracted-tongue-root
└── Prosodic
    ├── long_feature: long
    ├── nasalized_feature: nasalized
    ├── labialized_feature: labialized
    ├── palatalized_feature: palatalized
    ├── pharyngealized_feature: pharyngealized
    ├── ejective_feature: ejective
    └── stress_feature: primary-stress
```

Each leaf `FeatureNode` has a `name`, a `positive` value, and optionally a
`negative` value. Where the `negative` field is empty (`""`), the feature is
privative: it is either present or absent, with no explicit negative pole.

---

## Feature-to-Geometry Mapping

The `FEATURE_TO_GEOMETRY_NODE` dictionary maps feature values to their
parent geometry node names. This mapping drives the geometry-weighted distance
algorithm.

| Geometry Node | Feature Values |
|---------------|----------------|
| **Laryngeal** | voiced, voiceless, aspirated, glottalized, breathy, creaky |
| **Manner** | stop, fricative, affricate, nasal, approximant, trill, tap, lateral, click, implosive, sibilant, syllabic, non-syllabic |
| **Labial** | bilabial, labio-dental, labio-velar, labio-palatal, labial, rounded, unrounded |
| **Coronal** | dental, alveolar, post-alveolar, alveolo-palatal, retroflex, linguolabial |
| **Dorsal** | palatal, palatal-velar, velar, uvular, close, near-close, close-mid, mid, open-mid, near-open, open, front, near-front, central, near-back, back |
| **Pharyngeal** | pharyngeal, epiglottal |
| **Glottal** | glottal |
| **TongueRoot** | advanced-tongue-root, retracted-tongue-root |
| **Prosodic** | long, nasalized, labialized, palatalized, pharyngealized, ejective, primary-stress |

---

## Built-in Systems Summary

| System | Name | Kind | Features | Distance Method |
|--------|------|------|----------|-----------------|
| IPA | `"ipa"` | Categorical | Parsed from sound names | Geometry-weighted |
| Tresoldi | `"tresoldi"` | Categorical | Broader descriptive labels | Geometry-weighted |
| Distinctive | `"distinctive"` | Categorical + Scalar | 24+ scalar dimensions | Scalar-weighted |
| P-base HC | `"pbase-hc"` | Valued | Halle & Clements features | Mismatch ratio |
| P-base JFH | `"pbase-jfh"` | Valued | Jakobson/Fant/Halle features | Mismatch ratio |
| P-base SPE | `"pbase-spe"` | Valued | SPE features | Mismatch ratio |
| P-base UFTC | `"pbase-uftc"` | Valued | Unified Feature Theory features | Mismatch ratio |
