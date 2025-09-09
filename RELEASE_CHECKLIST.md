# Release Checklist

## Pre-release

- [ ] **Version Update**
  - [ ] Update version in `pyproject.toml`
  - [ ] Update version in `distfeat/__init__.py`
  - [ ] Update version in documentation

- [ ] **Code Quality**
  - [ ] Run `ruff check distfeat/` and fix issues
  - [ ] Run `black distfeat/` to format code
  - [ ] Run `mypy distfeat/` and address type issues
  - [ ] All tests pass: `pytest tests/`
  - [ ] Test coverage > 80%

- [ ] **Documentation**
  - [ ] README.md is up to date
  - [ ] API documentation is complete
  - [ ] Changelog/release notes prepared
  - [ ] Documentation builds successfully

- [ ] **Dependencies**
  - [ ] Dependency versions are appropriate
  - [ ] No unnecessary dependencies
  - [ ] Optional dependencies work correctly

## Build and Test

- [ ] **Package Building**
  - [ ] Clean build: `rm -rf dist/ build/ *.egg-info/`
  - [ ] Build package: `python -m build`
  - [ ] Check package: `twine check dist/*`
  - [ ] Install locally: `pip install dist/*.whl`
  - [ ] Test import: `python -c "import distfeat; print(distfeat.__version__)"`

- [ ] **Functionality Testing**
  - [ ] Basic functionality works after install
  - [ ] Data files are included and accessible
  - [ ] Examples in README work
  - [ ] All distance methods functional

## Release

- [ ] **Git**
  - [ ] All changes committed
  - [ ] Create release tag: `git tag v0.2.0`
  - [ ] Push tag: `git push origin v0.2.0`

- [ ] **PyPI Upload**
  - [ ] Test on Test PyPI first: `twine upload --repository testpypi dist/*`
  - [ ] Test install from Test PyPI
  - [ ] Upload to PyPI: `twine upload dist/*`
  - [ ] Verify on PyPI website

- [ ] **Post-Release**
  - [ ] Update conda-forge recipe (if applicable)
  - [ ] Announce release
  - [ ] Update documentation version
  - [ ] Plan next version

## Commands Reference

```bash
# Quality checks
ruff check distfeat/
black distfeat/
mypy distfeat/
pytest tests/ --cov=distfeat

# Build
python -m build
twine check dist/*

# Test install
pip install dist/distfeat-*.whl
python -c "import distfeat; print(distfeat.__version__)"

# Upload
twine upload --repository testpypi dist/*  # Test first
twine upload dist/*  # Production
```

## Version Numbering

- **Major** (X.0.0): Breaking changes, incompatible API changes
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, backwards compatible

Current: 0.2.0 (Minor release with new features)