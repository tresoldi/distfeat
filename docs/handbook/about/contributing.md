# Contributing

Contributions to `distfeat` are welcome. Whether you are fixing a typo
in the handbook, adding a new feature system, or improving test
coverage, the process follows standard open-source practice.

## Getting started

1. **Fork** the repository at
   <https://github.com/tresoldi/distfeat>.

2. **Clone** your fork and install the development dependencies:

    ```bash
    git clone https://github.com/<your-username>/distfeat.git
    cd distfeat
    pip install -e ".[dev]"
    ```

3. **Create a branch** for your work:

    ```bash
    git checkout -b my-feature
    ```

4. Make your changes, then run the checks described below.

## Running checks

### Tests

The test suite uses [pytest](https://docs.pytest.org/):

```bash
pytest
```

To include a coverage report:

```bash
pytest --cov=distfeat
```

### Linting

The project uses [ruff](https://docs.astral.sh/ruff/) for linting and
import sorting:

```bash
ruff check src/ tests/
```

To auto-fix what ruff can handle automatically:

```bash
ruff check --fix src/ tests/
```

### Type checking

Static type analysis is performed with
[mypy](https://mypy-lang.org/) in strict mode:

```bash
mypy src/distfeat/
```

## Submitting a pull request

1. Ensure all three checks (pytest, ruff, mypy) pass locally.
2. Push your branch to your fork.
3. Open a pull request against the `master` branch of
   `tresoldi/distfeat`.
4. Describe what your change does and why. If it addresses an open
   issue, reference the issue number.

## Code style

- Python 3.12+ idioms are preferred.
- Use dataclasses where appropriate.
- Follow the existing code conventions: src-layout, protocol-based
  architecture, and flat module hierarchy.
- Keep functions small and composable; prefer a functional style where
  it makes the intent clearer.

## Documentation

Handbook pages live in `docs/handbook/`. If you add or modify a chapter,
make sure the entry appears in the `nav` section of `mkdocs.yml` and
that any code examples are placed in the corresponding
`docs/handbook/examples/` subdirectory.

## Questions

If you are unsure whether a change is in scope, open an issue first to
discuss it.
