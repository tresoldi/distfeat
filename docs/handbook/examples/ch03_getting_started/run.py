"""Chapter 3: Getting Started with distfeat — tracked example."""

import distfeat

# --- Feature Lookup ---
print("=== Feature Lookup ===")
for grapheme in ["p", "b", "t", "d", "k", "g"]:
    features = distfeat.get_features(grapheme)
    print(f"/{grapheme}/: {sorted(features)}")

# --- Representations ---
print("\n=== Representations ===")
ipa_repr = distfeat.get_representation("p")
print(f"IPA: {type(ipa_repr).__name__}, features: {sorted(ipa_repr.values)}")
pbase_repr = distfeat.get_representation("p", system="pbase-hc")
print(f"P-base HC: {type(pbase_repr).__name__}, features: {len(pbase_repr.values)}")

# --- Systems ---
print("\n=== Available Systems ===")
print(distfeat.list_systems())

# --- Sound Classes ---
print("\n=== Sound Classes ===")
print(f"is_class('S'): {distfeat.is_class('S')}")
print(f"is_class('p'): {distfeat.is_class('p')}")
print(f"class_features('S'): {sorted(distfeat.get_class_features('S'))}")

# --- Distance ---
print("\n=== Distance ===")
pairs = [("p", "b"), ("p", "t"), ("t", "d"), ("k", "g"), ("p", "k")]
for a, b in pairs:
    d = distfeat.distance(a, b)
    print(f"d({a}, {b}) = {d:.4f}")
