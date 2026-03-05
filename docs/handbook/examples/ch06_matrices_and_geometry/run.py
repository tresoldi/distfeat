"""Chapter 6: Matrices and Geometry — tracked example."""

import distfeat

# --- Minimal Matrices ---
print("=== Minimal Matrix: p vs b ===")
m1 = distfeat.minimal_matrix(["p", "b"])
print(f"Columns: {m1.columns}")
print(distfeat.tabulate_matrix(m1))

print("\n=== Minimal Matrix: p b t d ===")
m2 = distfeat.minimal_matrix(["p", "b", "t", "d"])
print(f"Columns: {m2.columns}")
print(distfeat.tabulate_matrix(m2))

print("\n=== Minimal Matrix: all stops ===")
m3 = distfeat.minimal_matrix(["p", "b", "t", "d", "k", "g"])
print(f"Columns: {m3.columns}")
print(distfeat.tabulate_matrix(m3))

# --- Markdown rendering ---
print("\n=== Markdown Format ===")
print(distfeat.tabulate_matrix(m3, format="markdown"))

# --- Geometry Tree ---
print("\n=== Geometry Tree ===")
geo = distfeat.DEFAULT_GEOMETRY
print(f"Root: {geo.name}")
for child in geo.children:
    print(f"  {child.name}")

# --- Feature Distance ---
print("\n=== Feature Distance ===")
print(f"voiced-voiceless: {distfeat.feature_distance('voiced', 'voiceless')}")
print(f"voiced-bilabial: {distfeat.feature_distance('voiced', 'bilabial')}")
print(f"stop-fricative: {distfeat.feature_distance('stop', 'fricative')}")

# --- Geometry Traversal ---
print("\n=== Geometry Traversal ===")
node = geo.find_feature("voiced")
print(f"find_feature('voiced'): {node}")
parent = geo.find_parent("voiced")
print(f"Parent of 'voiced': {parent.name}")
siblings = geo.siblings_of("voiced")
print(f"Siblings of 'voiced': {sorted(siblings)}")
