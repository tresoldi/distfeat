# Chapter 8: The Romance Consonant Inventory

The previous chapters introduced distfeat's modules one at a time,
each illustrated with a handful of Latin or Romance consonants drawn
from the running example.  This chapter reverses the direction:
it starts from the full consonant inventories of Latin and five
daughter languages and uses distfeat to organize, compare, and
annotate them.  The result is a consolidated feature table that
Chapter 9 will mine for distance-based analysis of lenition.

---

## The Latin Consonant System

Classical Latin had a small, tightly structured consonant inventory.
Fifteen segments are generally accepted for the standard literary
language, though reconstructions of earlier or regional varieties
sometimes add or remove a sound or two.  For our purposes the
following set is sufficient:

> /p b t d k g f s h m n l r w j/

We can group them by manner of articulation, using distfeat to confirm
each segment's feature bundle:

```python
import distfeat

latin = ["p", "b", "t", "d", "k", "g",    # stops
         "f", "s", "h",                     # fricatives
         "m", "n",                          # nasals
         "l", "r",                          # liquids
         "w", "j"]                          # glides

for grapheme in latin:
    feats = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(feats)}")
```

The output confirms how distfeat classifies each segment in the
default IPA system:

```
/p/  ['bilabial', 'consonant', 'stop', 'voiceless']
/b/  ['bilabial', 'consonant', 'stop', 'voiced']
/t/  ['alveolar', 'consonant', 'stop', 'voiceless']
/d/  ['alveolar', 'consonant', 'stop', 'voiced']
/k/  ['consonant', 'stop', 'velar', 'voiceless']
/g/  ['consonant', 'stop', 'velar', 'voiced']
/f/  ['consonant', 'fricative', 'labio-dental', 'voiceless']
/s/  ['alveolar', 'consonant', 'fricative', 'sibilant', 'voiceless']
/h/  ['consonant', 'fricative', 'glottal', 'voiceless']
/m/  ['bilabial', 'consonant', 'nasal', 'voiced']
/n/  ['alveolar', 'consonant', 'nasal', 'voiced']
/l/  ['alveolar', 'approximant', 'consonant', 'lateral', 'voiced']
/r/  ['alveolar', 'consonant', 'trill', 'voiced']
/w/  ['approximant', 'consonant', 'labio-velar', 'voiced']
/j/  ['approximant', 'consonant', 'palatal', 'voiced']
```

A few points deserve notice.  Latin /r/ was a trill, not a tap, and
distfeat correctly assigns `trill` rather than `tap`.  The glides /w/
and /j/ receive `approximant` and place labels (`labio-velar`,
`palatal`) that will become relevant when we trace the palatalization
processes that generated new consonants in the daughters.  And /h/,
which was already weakening in Classical Latin and would be lost in
all five daughters, sits at the extreme edge of the system as a
voiceless glottal fricative---the most underspecified consonant in the
inventory.

### The Latin consonant feature table

We can build a minimal distinguishing matrix for the full Latin
inventory to see which features separate each segment from the rest:

```python
import distfeat

latin = ["p", "b", "t", "d", "k", "g",
         "f", "s", "h",
         "m", "n",
         "l", "r",
         "w", "j"]

matrix = distfeat.minimal_matrix(latin)
print(distfeat.tabulate_matrix(matrix, format="markdown"))
```

The resulting table encodes the contrastive structure of the Latin
system.  Manner distinctions (stop vs. fricative vs. nasal vs.
approximant vs. trill) interact with place (bilabial, alveolar, velar,
labio-dental, glottal, labio-velar, palatal) and voicing.  Every Latin
consonant occupies a unique cell in this matrix---no two segments
share the same feature signature, as expected for a well-formed
phonemic inventory.

---

## Five Daughter Inventories

The Romance languages inherited the Latin system and reshaped it under
pressures that ranged from subtle phonetic drift to wholesale category
collapse.  We survey five daughters, noting the innovations that each
brings to the consonant inventory.

### Italian

Italian is the most conservative of the five in its treatment of
obstruents.  The voiceless stops /p t k/ survive largely unchanged,
and the voiced stops /b d g/ remain in most positions.  The principal
innovation is the development of a full set of affricates:

```python
import distfeat

italian_innovations = ["ts", "dz", "tʃ", "dʒ"]
for grapheme in italian_innovations:
    feats = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(feats)}")
```

```
/ts/  ['affricate', 'alveolar', 'consonant', 'sibilant', 'voiceless']
/dz/  ['affricate', 'alveolar', 'consonant', 'sibilant', 'voiced']
/tʃ/  ['affricate', 'consonant', 'post-alveolar', 'sibilant', 'voiceless']
/dʒ/  ['affricate', 'consonant', 'post-alveolar', 'sibilant', 'voiced']
```

These affricates arose from the palatalization of Latin /k/ and /g/
before front vowels (Latin CENTUM > Italian /tʃento/) and from the
gemination and subsequent affrication of certain consonant clusters.
Italian also developed the palatal nasal /ɲ/ and the palatal lateral
/ʎ/ from Latin sequences involving /n/ and /l/ followed by /j/:

```python
import distfeat

for grapheme in ["ɲ", "ʎ"]:
    feats = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(feats)}")
```

```
/ɲ/  ['consonant', 'nasal', 'palatal', 'voiced']
/ʎ/  ['approximant', 'consonant', 'lateral', 'palatal', 'voiced']
```

### Spanish

Spanish underwent more extensive changes, particularly in intervocalic
position.  Two innovations stand out.  First, Latin intervocalic
voiceless stops became voiced (lenition, Stage 1), so that Latin
/p t k/ between vowels surface as /b d g/.  Second, the voicing
contrast in this position was partly neutralized because original
voiced stops weakened further to approximants [β ð ɣ] in many
environments, a phenomenon that is allophonic in modern standard
Spanish but reflects the same lenition trajectory we will formalize
in Chapter 9.

Spanish also developed /x/ from a chain of changes ultimately
traceable to Latin /f/ in word-initial position (Latin FILIUM >
Old Spanish /hiʒo/ > modern /ixo/), and /θ/ (in Castilian) from
Latin /k/ before front vowels via an intermediate affricate stage
(Latin CAELUM > /tsjelo/ > /θjelo/):

```python
import distfeat

spanish_innovations = ["x", "θ"]
for grapheme in spanish_innovations:
    feats = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(feats)}")
```

```
/x/  ['consonant', 'fricative', 'velar', 'voiceless']
/θ/  ['consonant', 'dental', 'fricative', 'voiceless']
```

The velar fricative /x/ fills the slot that /h/ occupied in Latin
(both are voiceless fricatives at the back of the oral cavity), while
/θ/ occupies a position between the Latin dental stop /t/ and the
alveolar fricative /s/.

### French

French is the most innovative daughter.  Intervocalic lenition
proceeded through the full chain---voicing, spirantization, and
deletion---so that many Latin consonants have disappeared entirely.
The journey from Latin LUPUM to French /lu/ passes through stages
that can be tracked as successive feature operations:

```python
import distfeat

# The lenition of /p/ in French
p_feats = distfeat.get_features("p")
print(f"Latin /p/:  {sorted(p_feats)}")

# Stage 1: voicing -> /b/
b_feats = distfeat.add_features(p_feats, frozenset({"voiced"}))
print(f"Stage 1 /b/: {sorted(b_feats)}")
print(f"  (= {distfeat.features_to_grapheme(b_feats)})")

# Stage 2: spirantization -> /β/
beta_feats = distfeat.add_features(b_feats, frozenset({"fricative"}))
print(f"Stage 2 /β/: {sorted(beta_feats)}")
print(f"  (= {distfeat.features_to_grapheme(beta_feats)})")

# Stage 3: deletion -> ∅
print("Stage 3: ∅  (segment lost)")
```

```
Latin /p/:  ['bilabial', 'consonant', 'stop', 'voiceless']
Stage 1 /b/: ['bilabial', 'consonant', 'stop', 'voiced']
  (= b)
Stage 2 /β/: ['bilabial', 'consonant', 'fricative', 'voiced']
  (= β)
Stage 3: ∅  (segment lost)
```

French also developed the voiced fricatives /v ʒ/ and the voiceless
postalveolar fricative /ʃ/, and lost /h/ entirely.  The net effect
was a system with fewer stops but more fricatives than Latin---a
typological signature of extreme lenition.

```python
import distfeat

french_fricatives = ["v", "ʃ", "ʒ"]
for grapheme in french_fricatives:
    feats = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(feats)}")
```

```
/v/  ['consonant', 'fricative', 'labio-dental', 'voiced']
/ʃ/  ['consonant', 'fricative', 'post-alveolar', 'sibilant', 'voiceless']
/ʒ/  ['consonant', 'fricative', 'post-alveolar', 'sibilant', 'voiced']
```

### Portuguese

Portuguese followed a lenition path similar to Spanish, with
intervocalic voiceless stops voicing (/p/ > /b/, /t/ > /d/, /k/ > /g/)
and original voiced stops weakening further.  Where Portuguese diverges
is in nasalization: Latin nasal consonants in coda position were
absorbed into the preceding vowel as nasalization, leaving traces in
the vowel system rather than the consonant inventory.  The consonant
system itself is broadly similar to Spanish, with palatals /ɲ/ and
/ʎ/ from Latin /nj/ and /lj/ sequences and the voiced fricatives
/v/ and /ʒ/:

```python
import distfeat

portuguese_key = ["ɲ", "ʎ", "v", "ʒ"]
for grapheme in portuguese_key:
    feats = distfeat.get_features(grapheme)
    print(f"/{grapheme}/  {sorted(feats)}")
```

```
/ɲ/  ['consonant', 'nasal', 'palatal', 'voiced']
/ʎ/  ['approximant', 'consonant', 'lateral', 'palatal', 'voiced']
/v/  ['consonant', 'fricative', 'labio-dental', 'voiced']
/ʒ/  ['consonant', 'fricative', 'post-alveolar', 'sibilant', 'voiced']
```

### Romanian

Romanian, like Italian, is conservative in its treatment of stops.
The voiceless series /p t k/ survives in most environments.  The main
consonantal innovation is the development of /ts/ from Latin /k/
before front vowels (Latin CENTUM > Romanian /tsint/), a change shared
with Italian but without the further shift to a postalveolar place
that Italian shows:

```python
import distfeat

ts_feats = distfeat.get_features("ts")
tsh_feats = distfeat.get_features("tʃ")
print(f"/ts/  {sorted(ts_feats)}")
print(f"/tʃ/  {sorted(tsh_feats)}")
```

```
/ts/  ['affricate', 'alveolar', 'consonant', 'sibilant', 'voiceless']
/tʃ/  ['affricate', 'consonant', 'post-alveolar', 'sibilant', 'voiceless']
```

The difference between Romanian /ts/ and Italian /tʃ/ is a single
place feature: `alveolar` vs. `post-alveolar`.  Both are voiceless
sibilant affricates.

---

## Innovations as Feature Operations

Each of the sound changes surveyed above can be modeled as a
well-defined operation on feature bundles.  The `add_features`
function replaces features within a category while preserving the
rest of the bundle, which is precisely what phonological rules do.

### Voicing

The most common lenition innovation across the daughters is
intervocalic voicing of stops.  This is a single-feature operation:

```python
import distfeat

p_feats = distfeat.get_features("p")
b_feats = distfeat.add_features(p_feats, frozenset({"voiced"}))
print(f"/p/ -> /b/: {sorted(p_feats)} -> {sorted(b_feats)}")
print(f"  grapheme: {distfeat.features_to_grapheme(b_feats)}")

t_feats = distfeat.get_features("t")
d_feats = distfeat.add_features(t_feats, frozenset({"voiced"}))
print(f"/t/ -> /d/: {sorted(t_feats)} -> {sorted(d_feats)}")
print(f"  grapheme: {distfeat.features_to_grapheme(d_feats)}")

k_feats = distfeat.get_features("k")
g_feats = distfeat.add_features(k_feats, frozenset({"voiced"}))
print(f"/k/ -> /g/: {sorted(k_feats)} -> {sorted(g_feats)}")
g_grapheme = distfeat.features_to_grapheme(g_feats)
print(f"  grapheme: {g_grapheme}")  # IPA U+0261 ɡ
```

```
/p/ -> /b/: ['bilabial', 'consonant', 'stop', 'voiceless'] -> ['bilabial', 'consonant', 'stop', 'voiced']
  grapheme: b
/t/ -> /d/: ['alveolar', 'consonant', 'stop', 'voiceless'] -> ['alveolar', 'consonant', 'stop', 'voiced']
  grapheme: d
/k/ -> /g/: ['consonant', 'stop', 'velar', 'voiceless'] -> ['consonant', 'stop', 'velar', 'voiced']
  grapheme: ɡ
```

In every case the operation flips `voiceless` to `voiced` and leaves
place and manner untouched.  The structural parallelism across
the three series is captured automatically by the feature algebra.

### Spirantization

Spirantization---the weakening of a stop to a fricative at the same
place of articulation---is the next step in the lenition chain.  It
operates on manner rather than laryngeal features:

```python
import distfeat

b_feats = distfeat.get_features("b")
beta_feats = distfeat.add_features(b_feats, frozenset({"fricative"}))
print(f"/b/ -> /β/: {sorted(b_feats)} -> {sorted(beta_feats)}")
print(f"  grapheme: {distfeat.features_to_grapheme(beta_feats)}")

# /d/ is alveolar, but /ð/ is dental---spirantization also shifts place.
d_feats = distfeat.get_features("d")
eth_feats = distfeat.add_features(d_feats, frozenset({"fricative", "dental"}))
print(f"/d/ -> /ð/: {sorted(d_feats)} -> {sorted(eth_feats)}")
print(f"  grapheme: {distfeat.features_to_grapheme(eth_feats)}")

g_feats = distfeat.get_features("g")
gamma_feats = distfeat.add_features(g_feats, frozenset({"fricative"}))
print(f"/g/ -> /ɣ/: {sorted(g_feats)} -> {sorted(gamma_feats)}")
print(f"  grapheme: {distfeat.features_to_grapheme(gamma_feats)}")
```

```
/b/ -> /β/: ['bilabial', 'consonant', 'stop', 'voiced'] -> ['bilabial', 'consonant', 'fricative', 'voiced']
  grapheme: β
/d/ -> /ð/: ['alveolar', 'consonant', 'stop', 'voiced'] -> ['consonant', 'dental', 'fricative', 'voiced']
  grapheme: ð
/g/ -> /ɣ/: ['consonant', 'stop', 'velar', 'voiced'] -> ['consonant', 'fricative', 'velar', 'voiced']
  grapheme: ɣ
```

Notice that the `add_features` call replaces `stop` with `fricative`
in the manner slot---it does not simply add `fricative` alongside
`stop`.  This is because `stop` and `fricative` belong to the same
category (`manner`) in distfeat's feature ontology, so the newer value
displaces the older.  The behavior matches the phonological
intuition that a segment cannot be simultaneously a stop and a
fricative (except in the special case of affricates, which have
their own label).

The coronal case requires a second feature in the `add_features`
call: `dental` alongside `fricative`.  This is because /d/ is
classified as `alveolar` while /ð/ is classified as `dental` in
the IPA feature table---spirantization of the coronal stop shifts
the sub-place slightly forward.  The labial and dorsal series do not
show this complication because their place features are preserved
unchanged through spirantization.

### Deletion as the limit case

The lenition chain terminates in deletion: /β/ > zero, /ð/ > zero,
/ɣ/ > zero.  Deletion is the one change that cannot be modeled as a
feature operation, because the result is not a segment at all.
distfeat does not attempt to represent the null segment.  This is a
deliberate design boundary: the library measures structure within
the space of existing segments, and deletion falls outside that space.
We will return to this point in Chapter 9 when computing cumulative
distances along the lenition chain.

---

## Building the Comparative Table

With the inventories and innovations in hand, we can build a
comparative table that aligns the reflexes of individual Latin
consonants across the five daughters.  The most revealing cases are
the intervocalic stops, where the daughters have diverged the most.

### Reflexes of Latin /p/

The fate of Latin intervocalic /p/ illustrates the lenition continuum.
Consider the etymon LUPUM 'wolf':

| Language   | Reflex  | Word form |
|------------|---------|-----------|
| Latin      | /p/     | LUPUM     |
| Italian    | /p/     | lupo      |
| Spanish    | /b/     | lobo      |
| French     | --      | loup      |
| Portuguese | /b/     | lobo      |
| Romanian   | /p/     | lup       |

Italian and Romanian retain /p/; Spanish and Portuguese voice it to
/b/; French has lost it entirely (the orthographic _p_ in _loup_ is
silent).  We can ask distfeat to build a minimal matrix from the set
of attested reflexes:

```python
import distfeat

# Reflexes of Latin /p/ (excluding deletion)
reflexes = ["p", "b"]
matrix = distfeat.minimal_matrix(reflexes)
print(distfeat.tabulate_matrix(matrix))
```

```
grapheme | voiced
---------+-------
p        | False
b        | True
```

The matrix confirms what the traditional account says: voicing alone
distinguishes the conservative reflex from the innovative one.

### Expanding the reflex set

If we include the intermediate fricative stage attested in French
(before final deletion) and the labio-dental /v/ that appears in some
Romance varieties and related contexts, the matrix grows:

```python
import distfeat

reflexes = ["p", "b", "β", "v"]
matrix = distfeat.minimal_matrix(reflexes)
print(distfeat.tabulate_matrix(matrix))
```

```
grapheme | bilabial | fricative | voiced
---------+----------+-----------+-------
p        | True     | False     | False
b        | True     | False     | True
β        | True     | True      | True
v        | False    | True      | True
```

Three features suffice to distinguish four reflexes.  The
`bilabial`/`labio-dental` contrast separates /v/ from /β/ (both are
voiced fricatives, but at different places), while `fricative` and
`voiced` encode the voicing and spirantization steps.  The matrix
gives a compressed picture of the innovations: each row's feature
signature tells us exactly which changes have applied.

### Reflexes of other Latin consonants

The same approach can be applied to any Latin consonant.  The
reflexes of Latin /k/ before front vowels are particularly
instructive:

| Language   | Reflex  | Etymon (CENTUM 'hundred') |
|------------|---------|---------------------------|
| Latin      | /k/     | CENTUM                    |
| Italian    | /tʃ/    | cento                     |
| Spanish    | /θ/     | ciento                    |
| French     | /s/     | cent                      |
| Portuguese | /s/     | cento                     |
| Romanian   | /ts/    | (suta)                    |

```python
import distfeat

k_reflexes = ["k", "tʃ", "θ", "s", "ts"]
matrix = distfeat.minimal_matrix(k_reflexes)
print(distfeat.tabulate_matrix(matrix))
```

The matrix reveals the dimensions along which the palatalization
outcome varies: place of articulation (velar, postalveolar, dental,
alveolar), manner (stop, affricate, fricative), and the presence or
absence of the `sibilant` feature.

### Etyma as comparative vectors

Each etymon defines a vector across the five daughters.  Consider
four core etyma:

| Etymon       | Gloss    | IT   | ES   | FR   | PT   | RO   |
|--------------|----------|------|------|------|------|------|
| LUPUM        | 'wolf'   | /p/  | /b/  | --   | /b/  | /p/  |
| VITAM        | 'life'   | /t/  | /d/  | --   | /d/  | /ts/ |
| FOCUM        | 'fire'   | /k/  | /g/  | /f/  | /g/  | /k/  |
| AMICUM       | 'friend' | /k/  | /g/  | --   | /g/  | /k/  |

Each row is a set of reflexes that can be fed to `minimal_matrix`.
Across the full set of etyma, the matrices reveal the same small
inventory of distinctive features recurring in different combinations.
This regularity is the formal content of the Neogrammarian hypothesis
that sound change is regular: the feature operations that distfeat
models apply uniformly across the lexicon, and the minimal matrices
capture the structural result.

---

## Summary

This chapter assembled the consonant inventories of Latin and five
Romance daughters, annotated each segment with its distfeat feature
bundle, modeled the major innovations as feature operations, and built
comparative matrices that compress the diachronic variation into a
small set of distinguishing features.  The data produced here---the
feature bundles, the operation sequences, the reflex sets---will be
the raw material for Chapter 9, where we formalize lenition as a
trajectory in feature space and measure its distance profile across
systems.

---

*Reference implementation: `examples/ch08_romance_inventory/`*
