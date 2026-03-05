# Task Recipes

Practical workflows for computational phonology and computational historical
linguistics.

## 1) Explore Candidate Correspondences

Goal: inspect likely segment correspondences between two inventories.

```python
import distfeat

lang_a = ["p", "t", "k", "b", "d", "g", "s", "m", "n", "l", "r", "a", "e", "i", "o", "u"]
lang_b = ["p", "t", "k", "b", "d", "g", "h", "m", "n", "l", "r", "a", "e", "i", "o", "u"]

pairs = []
for seg_a in lang_a:
    for seg_b in lang_b:
        d = distfeat.distance(seg_a, seg_b, system="ipa")
        pairs.append((seg_a, seg_b, d))

pairs.sort(key=lambda item: item[2])
for seg_a, seg_b, d in pairs[:20]:
    print(f"{seg_a} ~ {seg_b}: {d:.3f}")
```

Notes:

- switch to `system="distinctive"` for scalar-driven comparison
- for underspecified features, consider `system="pbase-hc"`

## 2) Build a Consonant Class Hypothesis

Goal: infer strict shared features for a proposed natural class.

```python
import distfeat

candidate = ["p", "t", "k"]
shared = distfeat.derive_class_features(candidate, system="ipa")
print(shared)
```

Interpretation:

- features in `shared` are the strict intersection
- if the set is too broad or too narrow, refine your candidate class

## 3) Find Inventory Gaps Relative to a Feature Profile

Goal: list segments matching a profile and compare with attested inventory.

```python
import distfeat

attested = {"p", "t", "k", "b", "d", "g", "m", "n", "s"}
target = frozenset({"consonant", "voiceless", "stop"})

all_matches = set(distfeat.features_to_graphemes(target, system="ipa"))
missing = sorted(all_matches - attested)

print("Candidates in system:", sorted(all_matches))
print("Missing in inventory:", missing)
```

## 4) Extract Minimal Contrasts for a Local Opposition

Goal: describe which features distinguish a local set of segments.

```python
import distfeat

matrix = distfeat.minimal_matrix(["t", "d", "s"], system="ipa")
print(distfeat.tabulate_matrix(matrix))
```

Use this when writing correspondence rules, sound change diagnostics, or
teaching materials.

## 5) Query P-base Multi-State Features

Goal: retrieve segments by explicit valued constraints.

```python
import distfeat

syllabic = distfeat.features_to_graphemes({"syllabic": "+"}, system="pbase-hc")
print(syllabic[:20])

obstruent_like = distfeat.features_to_graphemes(
    {"consonantal": "+", "sonorant": "-"},
    system="pbase-hc",
)
print(obstruent_like[:20])
```

## 6) Compare Two Candidate Reflexes in a Pipeline

Goal: score alternatives for downstream ranking.

```python
import distfeat

source = "t"
candidates = ["d", "s", "r"]

scores = [
    (cand, distfeat.distance(source, cand, system="distinctive"))
    for cand in candidates
]
scores.sort(key=lambda item: item[1])
print(scores)
```

For reproducibility, always report:

- `distfeat` version
- system name (for example `ipa` vs `distinctive` vs `pbase-hc`)
- any non-default query/distance assumptions
