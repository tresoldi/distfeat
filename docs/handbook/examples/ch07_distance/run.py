"""Chapter 7: Distance — tracked example."""

import distfeat

# --- System-Based Distance ---
print("=== Distance Across Systems ===")
for system in ["ipa", "distinctive"]:
    d = distfeat.distance("p", "b", system=system)
    print(f"d(p, b) [{system}]: {d:.4f}")

# --- Full 6x6 Distance Matrix (IPA) ---
print("\n=== 6x6 Distance Matrix (IPA) ===")
stops = ["p", "b", "t", "d", "k", "g"]
header = "       " + "  ".join(f"{s:>6}" for s in stops)
print(header)
for a in stops:
    row = f"/{a}/    "
    for b in stops:
        d = distfeat.distance(a, b)
        row += f"{d:>6.4f}  "
    print(row)

# --- Cross-System Comparison ---
print("\n=== Cross-System Comparison ===")
pairs = [("p", "b"), ("p", "t"), ("t", "d"), ("k", "g")]
for a, b in pairs:
    ipa_d = distfeat.distance(a, b, system="ipa")
    dist_d = distfeat.distance(a, b, system="distinctive")
    print(f"d({a},{b}):  ipa={ipa_d:.4f}  distinctive={dist_d:.4f}")

# --- Feature Distance ---
print("\n=== Feature Distance ===")
print(f"voiced vs voiceless: {distfeat.feature_distance('voiced', 'voiceless')}")
print(f"stop vs fricative:   {distfeat.feature_distance('stop', 'fricative')}")
