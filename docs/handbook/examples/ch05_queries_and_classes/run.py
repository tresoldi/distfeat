"""Chapter 5: Queries and Classes — tracked example."""

import distfeat

# --- Feature Queries ---
print("=== Feature Queries ===")
voiceless_stops = distfeat.features_to_graphemes(
    frozenset({"consonant", "stop", "voiceless", "bilabial"})
)
print(f"Voiceless bilabial stops: {voiceless_stops[:5]}")

# --- Negative Queries ---
print("\n=== Negative Queries ===")
stops_not_voiced = distfeat.features_to_graphemes(
    frozenset({"consonant", "stop", "-voiced"})
)
print(f"Stops (not voiced), first 5: {stops_not_voiced[:5]}")

# --- Derive Class Features ---
print("\n=== Derive Class Features ===")
shared_ptk = distfeat.derive_class_features(["p", "t", "k"])
print(f"p, t, k share: {sorted(shared_ptk)}")

shared_pb = distfeat.derive_class_features(["p", "b"])
print(f"p, b share: {sorted(shared_pb)}")

shared_bdg = distfeat.derive_class_features(["b", "d", "g"])
print(f"b, d, g share: {sorted(shared_bdg)}")

# --- Feature Composition ---
print("\n=== Feature Composition ===")
features_p = distfeat.get_features("p")
features_b = distfeat.add_features(features_p, frozenset({"voiced"}))
print(f"/p/ features: {sorted(features_p)}")
print(f"/p/ + voiced: {sorted(features_b)}")
print(f"/b/ features: {sorted(distfeat.get_features('b'))}")
print(f"Match: {features_b == distfeat.get_features('b')}")

# --- Sound Classes ---
print("\n=== Sound Classes ===")
for cls in ["C", "V", "S", "F", "N"]:
    if distfeat.is_class(cls):
        feats = distfeat.get_class_features(cls)
        print(f"Class {cls}: {sorted(feats)}")
