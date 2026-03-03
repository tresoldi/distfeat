# Part II: The Romance Consonant Workshop

<p class="part-title">A hands-on tour of the distfeat API</p>

Part II is a tutorial-style workshop. Each chapter pairs a core
phonological concept with the `distfeat` module that implements it,
using the Romance consonant inventory as the running dataset. Code
examples are self-contained: every listing can be copied into a script
and executed against the library's bundled data.

## Chapters

**[Chapter 4 --- Systems and Representations](ch04_systems_and_representations.md)**
introduces the four system families shipped with `distfeat`---IPA,
Tresoldi, Distinctive, and P-base---and shows how to convert between
graphemes and native representations. The Romance stops /p t k b d g/
serve as the first test set.

**[Chapter 5 --- Queries and Classes](ch05_queries_and_classes.md)**
covers natural-class queries: selecting all segments that share a
feature bundle, testing class membership, and deriving class features
from an arbitrary set of sounds. The chapter uses the full Romance
obstruent inventory to illustrate inclusive and exclusive queries.

**[Chapter 6 --- Matrices and Geometry](ch06_matrices_and_geometry.md)**
builds minimal-pair feature matrices and introduces the Clements and
Hume feature geometry tree that `distfeat` uses for weighted distance
calculations. The reader constructs a matrix for the Latin stop series
and inspects the geometry weights that distinguish place from manner
from laryngeal features.

**[Chapter 7 --- Distance](ch07_distance.md)** brings the previous
chapters together by computing pairwise segment distances across
multiple systems. The chapter demonstrates how different feature
systems yield different distance profiles for the same pair of segments,
and why that matters for alignment and cognate detection in historical
linguistics.

---

*After completing Part II the reader will be able to query any feature
system, build matrices, and compute distances using the full `distfeat`
API.*
