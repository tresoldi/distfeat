# Changelog

## 0.5.0

- Added task-oriented workflow recipes for computational phonology and
  computational historical linguistics.
- Added explicit methodological assumptions documentation for built-in systems.
- Added stable export helpers:
  `export_matrix(...)`, `export_distances(...)`, and `export_class_features(...)`.
- Added dataset quality audit APIs:
  `DatasetAuditReport` and `audit_dataset(...)`.
- Added explicit valued-feature uncertainty controls:
  `valued_matches(...)`, `valued_distance(...)`, and DOT-policy controls in
  `features_to_graphemes(...)` and `distance(...)` for valued systems.
- Changed `scripts/verify_examples.py` so metadata writes are opt-in
  (`--write-meta`) and verification is read-only by default.

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
