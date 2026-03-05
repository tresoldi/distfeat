"""Chapter 9: Modeling Western Romance Lenition — tracked example."""

import distfeat

# --- The Lenition Chain ---
print("=== Lenition Chains: Feature Bundles ===")
chains = {
    "labial":  ["p", "b", "β"],
    "coronal": ["t", "d", "ð"],
    "dorsal":  ["k", "g", "ɣ"],
}
for label, chain in chains.items():
    print(f"\n{label.upper()} chain:")
    for g in chain:
        feats = distfeat.get_features(g)
        print(f"  /{g}/: {sorted(feats)}")

# --- Feature Distance at Each Stage ---
print("\n=== Stage Distances (IPA) ===")
for label, chain in chains.items():
    print(f"\n{label}:")
    cumulative = 0.0
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        d = distfeat.distance(a, b)
        cumulative += d
        print(f"  Stage {i}→{i+1} ({a}→{b}): {d:.4f}")
    # Total chain distance
    d_total = distfeat.distance(chain[0], chain[-1])
    print(f"  Total ({chain[0]}→{chain[-1]}): {d_total:.4f}")

# --- Geometry-Weighted Analysis ---
print("\n=== Feature Distance (Geometry) ===")
print(f"voiced ↔ voiceless (Stage 0→1): {distfeat.feature_distance('voiced', 'voiceless')}")
print(f"stop ↔ fricative (Stage 1→2):   {distfeat.feature_distance('stop', 'fricative')}")

# --- Lenition Matrix ---
print("\n=== Lenition Matrix: p b β ===")
matrix = distfeat.minimal_matrix(["p", "b", "β"])
print(f"Columns: {matrix.columns}")
print(distfeat.tabulate_matrix(matrix))

# --- Distinctive Scalar Perspective ---
print("\n=== Scalar Trajectory (Distinctive) ===")
ds = distfeat.get_system("distinctive")
for g in ["p", "b", "β"]:
    scalars = ds.grapheme_to_scalars(g)
    key_dims = {k: scalars[k] for k in ["voice", "continuant"] if k in scalars}
    print(f"  /{g}/: {key_dims}")

# --- Symmetry ---
print("\n=== Distance Symmetry ===")
d_pb = distfeat.distance("p", "b")
d_bp = distfeat.distance("b", "p")
print(f"d(p,b) = {d_pb:.4f}")
print(f"d(b,p) = {d_bp:.4f}")
print(f"Symmetric: {d_pb == d_bp}")
