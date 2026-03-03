# Changelog

## 0.3.0

- Replaced the legacy codebase with the extracted standalone `distfeat` package.
- Established a clean `src/`-layout package with bundled TSV feature data.
- Added the new public API centered on datasets, registries, geometry, and the
  built-in `ipa`, `tresoldi`, and `distinctive` systems.
- Added functional top-level helpers for feature lookup, class lookup, and
  distance calculations.
- Added a standalone documentation set covering the API, datasets, systems, and
  development constraints.
- Added a focused test suite for dataset loading, registries, geometry, and the
  built-in systems.
- Updated package metadata for the standalone release workflow.
