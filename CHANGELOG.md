# Changelog

## 0.4.0

- Added native multi-state feature support through `FeatureState`,
  `CategoricalFeatures`, and `ValuedFeatures`.
- Generalized the feature-system protocol so non-set representations are
  first-class and can participate in the main registry.
- Added bundled P-base-derived systems: `pbase-hc`, `pbase-jfh`, `pbase-spe`,
  and `pbase-uftc`.
- Added valued-system query, class-derivation, matrix, and distance support to
  the analysis layer.
- Bundled the derived P-base data files and packaged their attribution and
  license materials alongside the code.
- Expanded the test suite and documentation to cover native multi-state
  systems.

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
