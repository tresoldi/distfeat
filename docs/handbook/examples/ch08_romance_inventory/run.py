"""Chapter 8: The Romance Consonant Inventory — tracked example."""

import distfeat

# --- Latin Consonant System ---
print("=== Latin Consonant Inventory ===")
latin = ["p", "b", "t", "d", "k", "g", "f", "s", "m", "n", "l", "r"]
for g in latin:
    feats = distfeat.get_features(g)
    print(f"/{g}/: {sorted(feats)}")

# --- Daughter language innovations ---
print("\n=== Romance Innovations as Feature Operations ===")

# Voicing: /p/ -> /b/ (Spanish/Portuguese intervocalic)
features_p = distfeat.get_features("p")
voiced_p = distfeat.add_features(features_p, frozenset({"voiced"}))
print(f"/p/ + voiced = {sorted(voiced_p)}")
print(f"  matches /b/: {voiced_p == distfeat.get_features('b')}")

# Spirantization: /b/ -> /β/ (Spanish allophonic)
features_b = distfeat.get_features("b")
spirant_b = distfeat.add_features(features_b, frozenset({"fricative"}))
print(f"/b/ + fricative = {sorted(spirant_b)}")
print(f"  matches /β/: {spirant_b == distfeat.get_features('β')}")

# --- Comparative Table ---
print("\n=== Reflexes of Latin /p/ ===")
# LUPUM 'wolf': Latin /p/ reflexes
reflexes = {
    "Latin": "p",
    "Italian": "p",
    "Spanish": "b",
    "French": "v",  # /p/ > /b/ > /v/ (extreme lenition in some positions)
    "Portuguese": "b",
}
for lang, g in reflexes.items():
    feats = distfeat.get_features(g)
    print(f"  {lang} /{g}/: {sorted(feats)}")

# --- Minimal Matrix of Reflexes ---
print("\n=== Minimal Matrix: p b v ===")
matrix = distfeat.minimal_matrix(["p", "b", "v"])
print(distfeat.tabulate_matrix(matrix))
