"""Chapter 4: Systems and Representations — tracked example."""

import distfeat

# --- Registry ---
print("=== Registry ===")
print("Systems:", distfeat.list_systems())
print("Default:", distfeat.get_system().name)

# --- IPA System ---
print("\n=== IPA Features (Latin Obstruents) ===")
for g in ["p", "t", "k", "b", "d", "g", "f", "s"]:
    feats = distfeat.get_features(g)
    print(f"/{g}/: {sorted(feats)}")

# --- Tresoldi System ---
print("\n=== Tresoldi Features ===")
for g in ["p", "b"]:
    feats = distfeat.get_features(g, system="tresoldi")
    print(f"/{g}/: {sorted(feats)}")

# --- Distinctive Scalar Layer ---
print("\n=== Distinctive Scalars ===")
ds = distfeat.get_system("distinctive")
for g in ["p", "b", "t", "d", "k", "g"]:
    scalars = ds.grapheme_to_scalars(g)
    non_zero = {k: v for k, v in scalars.items() if v != 0.0}
    print(f"/{g}/: {non_zero}")

# --- P-base Systems ---
print("\n=== P-base SPE Representation ===")
for g in ["p", "b", "t"]:
    repr_ = distfeat.get_representation(g, system="pbase-spe")
    if repr_:
        # Show first 5 features
        items = list(repr_.values.items())[:5]
        print(f"/{g}/: {dict(items)} ...")
