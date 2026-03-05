# Part I: Foundations

<p class="part-title">From phonological theory to running code</p>

Part I establishes the conceptual and practical groundwork that the rest
of the handbook builds on. It moves from theory through data design to a
first working session with the library.

## Chapters

**[Chapter 1 --- Features as Theory](ch01_features_as_theory.md)**
traces the intellectual genealogy of distinctive features from
Jakobson, Fant, and Halle (1952) through Chomsky and Halle's *SPE*
(1968) to the geometrical models of Clements and Hume (1995).
Understanding where feature systems come from clarifies the design
choices that `distfeat` makes and the trade-offs each built-in system
represents.

**[Chapter 2 --- From Phonemes to Bundles](ch02_from_phonemes_to_bundles.md)**
surveys the data representations available in `distfeat`: categorical
feature bundles (frozensets of signed feature strings), valued feature
dictionaries (feature-to-value mappings), and multi-state segment tables
derived from the P-base tradition. The chapter explains when and why a
user would choose one representation over another.

**[Chapter 3 --- Getting Started](ch03_getting_started.md)** is a
hands-on quickstart. It covers installation, first imports, and basic
operations---retrieving features for a grapheme, querying a sound class,
and computing a segment distance---so that the reader has a working
`distfeat` session before entering Part II.

---

*After completing Part I the reader will know why phonological features
are organized the way they are, how `distfeat` represents them
internally, and how to install and invoke the library for the first
time.*
