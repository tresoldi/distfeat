# Chapter 5: Queries and Classes

<p class="chapter-subtitle">Feature queries, matching, and natural classes</p>

The previous chapter showed how to look up the features of a single
grapheme. This chapter inverts the direction: given a set of features,
find every grapheme that satisfies them. That inversion---from segment
to class---is the foundation of natural-class reasoning in phonology.
A *natural class* is any set of sounds definable by a feature bundle
shorter than the list of its members. `distfeat` provides the query
functions that make this definition operational.

The chapter proceeds from simple feature queries through negative
matching and valued queries to class derivation, feature composition,
and the predefined sound classes shipped with the library. The running
example remains the Latin obstruent inventory.

---

## Feature Queries

The function `features_to_graphemes` takes a frozenset of features and
returns every grapheme in the system whose feature set is a superset of
the query. This is partial matching: the query features must all be
present in the target, but the target may contain additional features.

```python
import distfeat

voiceless_stops = distfeat.features_to_graphemes(
    frozenset({"consonant", "stop", "voiceless"})
)
print(voiceless_stops[:10])
# ['c', "c'", "c'ʲ", "c'ʷ", "c'ʷˤ", "c'ː", "c'ˤ", 'cʰ', 'cʰː', 'cʰˠ']
print(f"Total matches: {len(voiceless_stops)}")
# Total matches: 497
```

The query `{consonant, stop, voiceless}` matches every voiceless stop in
the database---plain, aspirated, ejective, labialized, palatalized, and
so on. To narrow the results, add more features to the query:

```python
import distfeat

# Voiceless bilabial stops only
bilabial_vl_stops = distfeat.features_to_graphemes(
    frozenset({"consonant", "stop", "voiceless", "bilabial"})
)
print(bilabial_vl_stops[:5])
# ['p', "p'", "p'ʲ", "p'ʲː", "p'ː"]
```

The more features in the query, the fewer graphemes match. This is the
defining trade-off of natural-class queries: specificity versus
generality.

### Negative queries

Elements in the query frozenset that begin with a hyphen are treated as
**negative features**: they exclude any grapheme that carries the
corresponding positive feature. This is distfeat's equivalent of the
phonological convention of writing a minus sign before a feature name.

```python
import distfeat

# Stop consonants that are NOT voiced
voiceless_stops = distfeat.features_to_graphemes(
    frozenset({"stop", "consonant", "-voiced"})
)

# Filter to single-character graphemes for readability
simple = sorted(g for g in voiceless_stops if len(g) == 1)
print(simple)
# ['c', 'k', 'p', 'q', 't', 'ȶ', 'ʈ', 'ʔ', 'ʡ']
```

The negative query `{stop, consonant, -voiced}` matches any stop
consonant whose feature set does *not* contain `voiced`. This is not
quite the same as querying for `{stop, consonant, voiceless}`, but for
the bundled dataset both queries return the same simple graphemes,
because every stop in the data is explicitly marked as either voiced or
voiceless.

Negative features are a powerful mechanism for excluding subclasses.
To select fricatives that are not sibilant:

```python
import distfeat

non_sibilant_fricatives = distfeat.features_to_graphemes(
    frozenset({"consonant", "fricative", "-sibilant"})
)
simple = sorted(g for g in non_sibilant_fricatives if len(g) == 1)
print(simple)
# Non-sibilant fricatives: f, h, x, etc.
```

---

## Exact vs. Partial Matching

By default, `features_to_graphemes` uses partial matching: the query
is a subset test. Setting `exact=True` switches to exact equality.

```python
import distfeat

# Partial: any sound that has at least these features
partial = distfeat.features_to_graphemes(
    frozenset({"consonant", "stop", "voiceless", "bilabial"})
)
print(f"Partial matches: {len(partial)}")
# Partial matches: many (includes aspirated, ejective, etc.)

# Exact: only sounds whose ENTIRE feature set equals this
exact = distfeat.features_to_graphemes(
    frozenset({"consonant", "stop", "voiceless", "bilabial"}),
    exact=True,
)
print(f"Exact matches: {exact}")
# Exact matches: ['p']
```

The exact query returns only /p/, because /p/ is the only grapheme in
the database whose feature set is precisely `{consonant, stop, voiceless,
bilabial}` with no additional features.

### The `partial_match` and `matches` functions

For programmatic use on individual feature sets rather than whole-inventory
scans, two lower-level functions are available:

```python
import distfeat

p_features = distfeat.get_features("p")
pattern = frozenset({"consonant", "stop"})

print(distfeat.partial_match(pattern, p_features))
# True --- pattern is a subset of p's features
```

`partial_match(pattern, target)` returns `True` when every positive
feature in `pattern` is present in `target` and no negative feature in
`pattern` is present in `target`. It is the same logic that
`features_to_graphemes` applies internally.

`matches(pattern, target)` works with the native representation types
(`CategoricalFeatures` or `ValuedFeatures`) and dispatches to the
appropriate system semantics:

```python
import distfeat

p_rep = distfeat.get_representation("p")
b_rep = distfeat.get_representation("b")
stop_pattern = distfeat.get_class_representation("S")

print(distfeat.matches(stop_pattern, p_rep))
# True --- /p/ is a stop
print(distfeat.matches(stop_pattern, b_rep))
# True --- /b/ is a stop
```

---

## Valued Queries

The P-base systems use a different query interface. Instead of a
frozenset, you pass a dictionary whose keys are feature names and whose
values are state symbols (`"+"`, `"-"`, etc.):

```python
import distfeat

# All segments with [+voice] in the Halle-Clements system
voiced = distfeat.features_to_graphemes(
    {"voice": "+"},
    system="pbase-hc",
)
print(f"Voiced segments (pbase-hc): {len(voiced)}")
# Voiced segments (pbase-hc): 642

print(voiced[:10])
# First 10 matches
```

You can combine multiple features in the dictionary to narrow the query:

```python
import distfeat

# Voiceless non-continuant non-sonorant segments in P-base HC
voiceless_stops_hc = distfeat.features_to_graphemes(
    {"voice": "-", "continuant": "-", "sonorant": "-"},
    system="pbase-hc",
)
print(f"Voiceless stops (pbase-hc): {len(voiceless_stops_hc)}")
# Voiceless stops (pbase-hc): 302
```

Valued queries are matched using the system's `matches` method, which
checks that every key in the query dictionary has the specified value in
the target segment's representation.

---

## Deriving Shared Features

Given a set of graphemes, `derive_class_features` computes the
intersection of their feature sets---the features that every member
shares. This is the defining feature bundle of the natural class to which
those sounds belong.

```python
import distfeat

# What do /p/, /t/, and /k/ share?
shared = distfeat.derive_class_features(["p", "t", "k"])
print(shared)
# frozenset({'consonant', 'stop', 'voiceless'})
```

The result `{consonant, stop, voiceless}` is exactly the traditional
characterization of the voiceless stop class. The function has derived
the natural class from the data.

```python
import distfeat

# What do /p/ and /b/ share?
shared = distfeat.derive_class_features(["p", "b"])
print(shared)
# frozenset({'bilabial', 'consonant', 'stop'})
```

/p/ and /b/ share place (bilabial) and manner (stop) but differ in
voicing, so `voiceless` and `voiced` are absent from the intersection.
The shared bundle `{bilabial, consonant, stop}` defines the class of
bilabial stops regardless of phonation.

### Deriving valued shared features

For P-base systems, `derive_class_features` returns a dictionary of
feature-state pairs rather than a frozenset:

```python
import distfeat

shared_spe = distfeat.derive_class_features(
    ["p", "t", "k"],
    system="pbase-spe",
)
# Returns a dict of features where all three agree
for feature, state in sorted(shared_spe.items())[:8]:
    print(f"  {feature}: {state.value}")
```

The output shows only those SPE features for which /p/, /t/, and /k/
have identical values. Features where they disagree (such as `coronal`
or `high`) are excluded.

---

## Feature Composition

The function `add_features` takes a base feature set and a set of
features to add, returning a new frozenset. Crucially, the operation is
**category-aware**: if the added feature belongs to the same phonological
category as an existing feature, the old feature is replaced.

```python
import distfeat

p_features = distfeat.get_features("p")
print(f"/p/ features: {sorted(p_features)}")
# /p/ features: ['bilabial', 'consonant', 'stop', 'voiceless']

# Add voicing
modified = distfeat.add_features(p_features, frozenset({"voiced"}))
print(f"After adding 'voiced': {sorted(modified)}")
# After adding 'voiced': ['bilabial', 'consonant', 'stop', 'voiced']

# Verify this matches /b/
b_features = distfeat.get_features("b")
print(f"/b/ features: {sorted(b_features)}")
print(f"Modified == /b/: {modified == b_features}")
# Modified == /b/: True
```

The key behavior is on the third line: adding `voiced` automatically
removed `voiceless`, because both belong to the `phonation` category.
Without this category awareness, the result would have been the
contradictory set `{bilabial, consonant, stop, voiceless, voiced}`.

### Modeling sound change

Feature composition is the mechanism for modeling sound change as feature
addition. The Western Romance lenition of intervocalic voiceless stops
can be expressed as:

```python
import distfeat

# Latin intervocalic voiceless stops undergo voicing
latin_voiceless = ["p", "t", "k"]

for grapheme in latin_voiceless:
    original = distfeat.get_features(grapheme)
    lenited = distfeat.add_features(original, frozenset({"voiced"}))
    result = distfeat.features_to_grapheme(lenited)
    print(f"/{grapheme}/ + voiced -> /{result}/")
```

Output:

```
/p/ + voiced -> /b/
/t/ + voiced -> /d/
/k/ + voiced -> /g/
```

The function `features_to_grapheme` (singular) performs the reverse
lookup: given a complete feature set, it returns the unique grapheme
whose features match exactly, or `None` if no match exists.

### Changing place of articulation

Category replacement works for any phonological category:

```python
import distfeat

t_features = distfeat.get_features("t")
print(f"/t/ features: {sorted(t_features)}")
# /t/ features: ['alveolar', 'consonant', 'stop', 'voiceless']

# Change place from alveolar to bilabial
modified = distfeat.add_features(t_features, frozenset({"bilabial"}))
print(f"After adding 'bilabial': {sorted(modified)}")
# After adding 'bilabial': ['bilabial', 'consonant', 'stop', 'voiceless']

result = distfeat.features_to_grapheme(modified)
print(f"Result: /{result}/")
# Result: /p/
```

Adding `bilabial` replaced `alveolar` because both belong to the `place`
category. The result is the feature bundle for /p/.

---

## Sound Classes

`distfeat` ships with over 20 predefined sound classes---conventional
single-letter or multi-letter abbreviations for common natural classes.
These are loaded from the bundled dataset and are available in the
categorical systems (IPA, Tresoldi, Distinctive).

### Testing class membership

The function `is_class` tests whether a symbol is a predefined class
rather than a concrete grapheme:

```python
import distfeat

print(distfeat.is_class("S"))    # True --- "S" is the stop class
print(distfeat.is_class("V"))    # True --- "V" is the vowel class
print(distfeat.is_class("C"))    # True --- "C" is the consonant class
print(distfeat.is_class("p"))    # False --- "p" is a grapheme, not a class
print(distfeat.is_class("b"))    # False
```

### Retrieving class features

Each class symbol maps to a feature bundle that defines the class:

```python
import distfeat

stop_features = distfeat.get_class_features("S")
print(f"S (stop):      {stop_features}")
# S (stop):      frozenset({'stop'})

vowel_features = distfeat.get_class_features("V")
print(f"V (vowel):     {vowel_features}")
# V (vowel):     frozenset({'vowel'})

consonant_features = distfeat.get_class_features("C")
print(f"C (consonant): {consonant_features}")
# C (consonant): frozenset({'consonant'})

nasal_features = distfeat.get_class_features("N")
print(f"N (nasal):     {nasal_features}")
# N (nasal):     frozenset({'consonant', 'nasal'})
```

Notice that the nasal class `N` requires both `consonant` and `nasal`,
while the stop class `S` requires only `stop`. This reflects
conventional usage: "nasals" in phonological shorthand almost always
means nasal consonants, not nasalized vowels.

### Predefined class inventory

The complete set of predefined classes in the bundled dataset:

| Class | Features | Description |
| --- | --- | --- |
| A | affricate | Affricates |
| B | vowel, back | Back vowels |
| C | consonant | All consonants |
| CV | consonant, voiced | Voiced consonants |
| E | vowel, front | Front vowels |
| F | fricative | Fricatives |
| H | glottal | Glottal segments |
| K | velar | Velar segments |
| L | lateral | Laterals |
| N | consonant, nasal | Nasal consonants |
| P | bilabial | Bilabial segments |
| Q | uvular | Uvular segments |
| R | consonant, -stop | Non-stop consonants |
| S | stop | Stops |
| SV | stop, voiced | Voiced stops |
| SVL | stop, voiceless | Voiceless stops |
| V | vowel | All vowels |
| VL | vowel, long | Long vowels |
| VN | vowel, nasalized | Nasalized vowels |

Note the class `R`: its feature bundle `{consonant, -stop}` uses a
negative feature. It matches any consonant that is not a stop---the
traditional "resonant" or "non-obstruent" class. This is the same
negative-feature syntax available in `features_to_graphemes`.

### Class features as queries

Because class features are ordinary frozensets, they can be passed
directly to `features_to_graphemes`:

```python
import distfeat

stop_features = distfeat.get_class_features("S")
all_stops = distfeat.features_to_graphemes(stop_features)
print(f"Total stops in database: {len(all_stops)}")
# Total stops in database: 954
```

---

## Building the Romance Obstruent Inventory

The tools introduced in this chapter---queries, negative features, exact
matching, class features, and feature composition---are sufficient to
assemble the Latin obstruent consonant inventory from first principles.

### Step 1: Retrieve all voiceless stops at the three Latin places

```python
import distfeat

voiceless_stops = {}
for place in ["bilabial", "alveolar", "velar"]:
    matches = distfeat.features_to_graphemes(
        frozenset({"consonant", "stop", "voiceless", place}),
        exact=True,
    )
    if matches:
        voiceless_stops[place] = matches[0]
        print(f"Voiceless {place} stop: /{matches[0]}/")

# Output:
# Voiceless bilabial stop: /p/
# Voiceless alveolar stop: /t/
# Voiceless velar stop: /k/
```

### Step 2: Derive the voiced counterparts by composition

```python
import distfeat

voiceless = ["p", "t", "k"]

for grapheme in voiceless:
    features = distfeat.get_features(grapheme)
    voiced_features = distfeat.add_features(features, frozenset({"voiced"}))
    voiced_grapheme = distfeat.features_to_grapheme(voiced_features)
    print(f"/{grapheme}/ -> /{voiced_grapheme}/")

# Output:
# /p/ -> /b/
# /t/ -> /d/
# /k/ -> /g/
```

### Step 3: Add the fricatives

```python
import distfeat

# Voiceless labio-dental fricative
f_matches = distfeat.features_to_graphemes(
    frozenset({"consonant", "fricative", "voiceless", "labio-dental"}),
    exact=True,
)
print(f"Voiceless labio-dental fricative: /{f_matches[0]}/")
# Voiceless labio-dental fricative: /f/

# Voiceless alveolar sibilant fricative
s_matches = distfeat.features_to_graphemes(
    frozenset({"consonant", "fricative", "voiceless", "alveolar", "sibilant"}),
    exact=True,
)
print(f"Voiceless alveolar sibilant fricative: /{s_matches[0]}/")
# Voiceless alveolar sibilant fricative: /s/
```

### Step 4: Verify the full inventory as a natural class

```python
import distfeat

latin_obstruents = ["p", "t", "k", "b", "d", "g", "f", "s"]

# What features do ALL eight share?
shared = distfeat.derive_class_features(latin_obstruents)
print(f"Shared features: {shared}")
# Shared features: frozenset({'consonant'})

# What about just the stops?
stop_shared = distfeat.derive_class_features(["p", "t", "k", "b", "d", "g"])
print(f"Stop shared features: {stop_shared}")
# Stop shared features: frozenset({'consonant', 'stop'})

# Voiceless stops only
vl_shared = distfeat.derive_class_features(["p", "t", "k"])
print(f"Voiceless stop shared features: {vl_shared}")
# Voiceless stop shared features: frozenset({'consonant', 'stop', 'voiceless'})
```

The results confirm the classical analysis: /p t k b d g/ form the
natural class of stops (`{consonant, stop}`), /p t k/ form the voiceless
stops (`{consonant, stop, voiceless}`), and all eight together share only
`{consonant}`---they are obstruents, but the bundled dataset does not
include an explicit `obstruent` label, so the intersection reduces to
the type category alone.

### The full picture

Combining queries and composition, we can produce the entire Latin
obstruent grid programmatically:

```python
import distfeat

places = ["bilabial", "alveolar", "velar", "labio-dental"]
manners = ["stop", "fricative"]
phonations = ["voiceless", "voiced"]

print(f"{'':>12} {'voiceless':>12} {'voiced':>12}")
print("-" * 38)

for manner in manners:
    for place in places:
        row = f"{place:>12}"
        for phonation in phonations:
            query = frozenset({"consonant", manner, phonation, place})
            results = distfeat.features_to_graphemes(query, exact=True)
            grapheme = results[0] if results else "---"
            row += f" {grapheme:>12}"
        if any(
            distfeat.features_to_graphemes(
                frozenset({"consonant", manner, ph, place}), exact=True
            )
            for ph in phonations
        ):
            print(row)
```

This produces the familiar grid of Latin obstruents, assembled entirely
from feature queries rather than hand-curated lists.

---

*Tracked examples for this chapter are collected in
`examples/ch05_queries_and_classes/`.*
