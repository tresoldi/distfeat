# About distfeat

`distfeat` is developed by **Tiago Tresoldi** and released under the
[MIT License](license.md).

The library provides phonological feature systems for computational
historical linguistics. It is designed as a zero-dependency Python
package, requiring Python 3.12 or later, and follows a protocol-based
architecture that allows multiple feature system families to coexist
under a single interface.

## Links

- **Source code:** <https://github.com/tresoldi/distfeat>
- **Issue tracker:** <https://github.com/tresoldi/distfeat/issues>
- **PyPI:** (forthcoming)

## Design principles

`distfeat` is guided by a small set of engineering principles:

- **Zero runtime dependencies.** The package installs without pulling
  in any third-party libraries. Development tools (pytest, ruff, mypy)
  are optional extras.
- **Protocol-based architecture.** Feature systems conform to a
  `FeatureSystem` protocol rather than inheriting from a shared base
  class. This keeps the type hierarchy flat and makes it straightforward
  to add new systems.
- **Bundled data.** All feature datasets ship inside the package as
  plain TSV files, so the library works offline and without network
  access.
- **Scholarly grounding.** The feature geometry and distance logic draw
  on the Clements and Hume (1995) tradition, and every built-in system
  maps to a published or widely used feature framework.

## See also

- [Contributing](contributing.md)
- [Changelog](changelog.md)
- [License](license.md)
