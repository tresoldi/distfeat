# Changelog

All notable changes to `distfeat` are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
the project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## 0.4.0

### Added

- The distfeat Handbook: a scholarly handbook for phonological feature
  systems, organized in three parts (Foundations, Romance Consonant
  Workshop, Synthesis) with a reference section.
- Protocol-based `FeatureSystem` architecture with registry pattern.
- Four built-in system families: IPA, Tresoldi, Distinctive, and
  P-base (four variants).
- Feature geometry and weighted distance metrics based on Clements and
  Hume (1995).
- Analysis layer: natural-class queries, minimal-pair matrices,
  segment distance.
- Bundled P-base segment tables as native multi-state feature systems.
- MkDocs Material site with macros for tracked, reproducible code
  examples.

### Changed

- Extracted `distfeat` from `alteruphono` as a standalone,
  zero-dependency package.

---

*Earlier development history is recorded in the `alteruphono` repository.*
