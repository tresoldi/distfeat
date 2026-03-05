# Changelog

All notable changes to `distfeat` are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
the project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## 0.5.0

### Added

- Task-oriented recipes for computational phonology and historical-linguistic
  workflows.
- Explicit methodological-assumptions sections for each built-in system.
- Stable export APIs for matrices, distance maps, and class-feature outputs.
- Dataset audit/report APIs for coverage and consistency diagnostics.
- Valued-feature uncertainty controls for matching and distance.

### Changed

- Example verification is now read-only by default; metadata updates are
  opt-in via `--write-meta`.

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
