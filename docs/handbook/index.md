# The distfeat Handbook

**Version {{ version() }}**

---

`distfeat` is a phonological feature system library for computational
historical linguistics. It provides protocol-based access to multiple
feature representations---categorical bundles, valued dictionaries, and
multi-state segment tables---together with geometry-aware distance
metrics, natural-class queries, and minimal-pair matrices. The library
ships with zero runtime dependencies and targets Python 3.12 and above.

This handbook serves two audiences that meet at the same crossroads:
phonologists entering computation and computational linguists entering
phonology. Rather than treating either discipline as prerequisite, the
text builds both threads in parallel, so that each chapter delivers
usable theory *and* runnable code.

## The Romance consonant thread

A sustained worked example runs through the entire handbook: the
consonant inventory of the major Western Romance languages---Italian,
Spanish, French, Portuguese, and Romanian---as they descend from Latin.
This thread was chosen because it is empirically rich, well documented
in the comparative literature, and small enough to fit comfortably in a
tutorial. By the final chapter the reader will have modeled lenition
paths, computed segment distances, and built a full feature matrix for
the shared inventory.

## Structure

The handbook is organized in three parts, followed by reference material.

**[Part I: Foundations](part1/index.md)** introduces the intellectual
genealogy of distinctive features, surveys the data representations that
`distfeat` supports, and walks through a first coding session with the
library.

**[Part II: The Romance Consonant Workshop](part2/index.md)** is a
systematic, hands-on tour of the library's core modules. Each chapter
pairs a phonological concept---systems, natural classes, geometry,
distance---with the corresponding `distfeat` API, using the Romance
consonant data throughout.

**[Part III: Synthesis](part3/index.md)** brings the pieces together in
two case-study chapters: assembling the full Romance consonant inventory
and modeling Western Romance lenition as a distance-minimizing process.

The **[Reference](reference/index.md)** section provides the API
reference, a feature catalog, a glossary, and troubleshooting notes.

Information about the project, its contributors, and its license can be
found under **[About](about/index.md)**.
