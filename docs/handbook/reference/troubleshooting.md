# Troubleshooting

Common issues and their solutions when working with distfeat.

---

## Unknown Grapheme

**Symptom:** `get_features("X")` returns `None`, or `distance` raises
`KeyError: "Unknown grapheme or sound class: 'X'"`.

**Cause:** The grapheme is not in the dataset, or it uses a non-standard
Unicode encoding.

**Solutions:**

1. Check the grapheme is valid IPA. distfeat normalizes input to NFD and
   resolves common IPA equivalences (e.g., U+0261 ɡ → g), but novel symbols
   are not supported.

2. Verify with `list_graphemes`:

    ```python
    sys = distfeat.get_system()
    "ʃ" in sys.list_graphemes()  # True if supported
    ```

3. If using a P-base system, note that coverage may differ from the IPA
   system. Not all graphemes have P-base entries.

---

## System Mismatch

**Symptom:** `features_to_graphemes` raises `NotImplementedError` about
query type.

**Cause:** Categorical systems expect `frozenset[str]` queries; valued
systems (P-base) expect `dict[str, FeatureState | str]` queries.

**Solution:** Match the query type to the system:

```python
# Categorical system (ipa, tresoldi, distinctive)
distfeat.features_to_graphemes(frozenset({"consonant", "stop"}))

# Valued system (pbase-*)
distfeat.features_to_graphemes({"voice": "+"}, system="pbase-hc")
```

---

## Unexpected Distance Values

**Symptom:** Distance values differ across systems for the same grapheme
pair.

**Cause:** Each system uses a different distance algorithm:

- **IPA / Tresoldi:** Geometry-weighted, based on feature set differences
  weighted by tree depth.
- **Distinctive:** Scalar dimension differences, weighted by geometry
  mapping.
- **P-base:** Mismatch ratio: count of differing features divided by
  comparable features.

**Solution:** This is expected behavior. Different feature traditions encode
different information and weight it differently. Compare within a single
system for consistent results, or use cross-system comparison deliberately
(see [Ch. 7](../part2/ch07_distance.md)).

---

## Python Version

**Symptom:** `SyntaxError` or `ImportError` on import.

**Cause:** distfeat requires Python 3.12 or later. It uses `type` statement
syntax and `StrEnum`, both introduced in Python 3.12.

**Solution:** Upgrade Python:

```bash
python --version  # Must be 3.12+
```

---

## Registry State

**Symptom:** A previously registered system is not found, or the default
system has changed unexpectedly.

**Cause:** The global registry is mutable. Calls to `register`,
`set_default`, or `set_registry` modify shared state.

**Solutions:**

1. Use `reset_registry()` to restore the default state:

    ```python
    distfeat.reset_registry()
    ```

2. Use an isolated registry for testing or experimentation:

    ```python
    reg = distfeat.create_registry()
    # Work with reg without affecting the global state
    ```

---

## Empty Feature Sets

**Symptom:** `get_features` returns an empty `frozenset()`.

**Cause:** The grapheme exists in the dataset but has no features in the
NAME field that map to known feature values.

**Solution:** Check the sound name in the dataset:

```python
ds = distfeat.load_builtin_dataset()
ds.sounds.get("X")  # Returns the NAME string or None
```

---

## Minimal Matrix Returns No Columns

**Symptom:** `minimal_matrix` returns a `FeatureMatrix` with an empty
`columns` tuple.

**Cause:** Only one grapheme was provided, or all provided graphemes have
identical features.

**Solution:** Ensure the grapheme list contains at least two distinct
segments:

```python
matrix = distfeat.minimal_matrix(["p", "b"])  # At least 2 distinct segments
```

---

## Sound Classes vs. Graphemes

**Symptom:** `get_features("S")` returns the features of the sound class
"stops" rather than a grapheme.

**Cause:** Uppercase single letters are typically sound class symbols in the
dataset. `is_class("S")` returns `True`.

**Solution:** Use `is_class` to check whether a symbol is a class before
lookup. Sound classes and graphemes occupy separate namespaces but are
queried through the same functions.

```python
if distfeat.is_class("S"):
    features = distfeat.get_class_features("S")
else:
    features = distfeat.get_features("S")
```

---

## Import Errors for System Classes

**Symptom:** Cannot import `IPAFeatureSystem` or other system classes.

**Solution:** All public classes are available from the top-level package:

```python
from distfeat import (
    IPAFeatureSystem,
    TresoldiFeatureSystem,
    DistinctiveFeatureSystem,
    PBaseFeatureSystem,
)
```

---

## Precomputed Distance Lookup Failure

**Symptom:** `distance` raises `KeyError` about missing precomputed pair.

**Cause:** The `precomputed` dictionary does not contain the requested pair
in either direction.

**Solution:** The dictionary is checked both ways (`(a, b)` and `(b, a)`),
but both keys must be at the top level. Structure as nested dicts:

```python
precomputed = {
    "a": {"e": 0.3},
    "e": {"a": 0.3},  # Include reverse if needed
}
distfeat.distance("a", "e", precomputed=precomputed)
```
