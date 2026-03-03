# Development

Implementation notes for the `distfeat` subproject.

## Design Constraints

- the package uses a `src/` layout
- the default global registry should remain lazily initialized
- `distfeat` should stay dependency-free

Additional constraints:

- prefer a functional-first public API
- use dataclasses for core data structures
- keep the protocol narrow
- avoid hidden cross-package coupling to `alteruphono`

## Architecture

Core modules:

- `distfeat.dataset`: `FeatureDataset` and dataset loaders
- `distfeat.resources`: low-level TSV reading
- `distfeat.protocol`: `FeatureSystem`
- `distfeat.geometry`: feature hierarchy and distance logic
- `distfeat.common`: shared implementation helpers
- `distfeat.registry`: explicit registries plus lazy global registry
- `distfeat.systems.*`: built-in system implementations

## State Model

The package supports two usage styles:

- explicit `Registry` instances for isolated state
- a convenience default registry for simple scripts

The default registry must remain lazy to keep import side effects low and make
tests easier to reason about.

## Non-Goals

For the current extraction phase:

- no plugin system
- no `Sound` object
- no compatibility shim for `alteruphono.features`
- no generalized public API for user-defined geometry trees

## Standalone Layout

This repository uses a standard `src/` layout:

- `pyproject.toml` is the authoritative package config
- the package source lives under `src/distfeat/`
- tests live under `tests/`
- documentation pages live under `docs/`
