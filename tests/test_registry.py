"""Tests for registry APIs."""

from distfeat import (
    Registry,
    get_registry,
    get_system,
    list_systems,
    load_builtin_dataset,
    reset_registry,
    set_default,
)
from distfeat.registry import create_registry


def test_registry_creation() -> None:
    """Explicit registries can be created with built-ins."""
    registry = create_registry()
    assert isinstance(registry, Registry)
    assert "ipa" in registry.list_systems()


def test_lazy_default_registry() -> None:
    """The default registry is created lazily and exposes built-ins."""
    reset_registry()
    assert "ipa" in list_systems()
    assert get_registry().get_system().name == "ipa"


def test_set_default() -> None:
    """The default system can be changed on the global registry."""
    reset_registry()
    set_default("tresoldi")
    assert get_system().name == "tresoldi"
    set_default("ipa")


def test_explicit_registry_is_isolated() -> None:
    """An explicit registry maintains its own default setting."""
    registry = Registry(dataset=load_builtin_dataset())
    assert registry.list_systems() == []
