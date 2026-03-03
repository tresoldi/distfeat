"""Registry APIs for feature systems."""

from __future__ import annotations

from dataclasses import dataclass, field

from distfeat.dataset import FeatureDataset, load_builtin_dataset
from distfeat.protocol import FeatureSystem
from distfeat.representations import FeatureRepresentation
from distfeat.systems.distinctive import DistinctiveFeatureSystem
from distfeat.systems.ipa import IPAFeatureSystem
from distfeat.systems.pbase import PBaseFeatureSystem
from distfeat.systems.tresoldi import TresoldiFeatureSystem


@dataclass
class Registry:
    """Mutable registry of named feature systems bound to a dataset."""

    dataset: FeatureDataset
    systems: dict[str, FeatureSystem] = field(default_factory=dict)
    default_system: str = "ipa"

    def register(self, name: str, system: FeatureSystem) -> None:
        """Register a system under a name."""
        self.systems[name] = system

    def get_system(self, name: str | None = None) -> FeatureSystem:
        """Return the named system, or the current default."""
        key = name or self.default_system
        if key not in self.systems:
            msg = f"Unknown feature system: {key!r}. Available: {list(self.systems)}"
            raise KeyError(msg)
        return self.systems[key]

    def list_systems(self) -> list[str]:
        """List registered system names."""
        return list(self.systems)

    def set_default(self, name: str) -> None:
        """Set the default system by name."""
        if name not in self.systems:
            msg = f"Unknown feature system: {name!r}. Available: {list(self.systems)}"
            raise KeyError(msg)
        self.default_system = name


def create_registry(
    dataset: FeatureDataset | None = None,
    *,
    register_builtin: bool = True,
    default_system: str = "ipa",
) -> Registry:
    """Create a registry, optionally populated with built-in systems."""
    dataset_obj = dataset or load_builtin_dataset()
    registry = Registry(dataset=dataset_obj, default_system=default_system)
    if register_builtin:
        registry.register("ipa", IPAFeatureSystem(dataset_obj))
        registry.register("tresoldi", TresoldiFeatureSystem(dataset_obj))
        registry.register("distinctive", DistinctiveFeatureSystem(dataset_obj))
        registry.register("pbase-hc", PBaseFeatureSystem("hc"))
        registry.register("pbase-jfh", PBaseFeatureSystem("jfh"))
        registry.register("pbase-spe", PBaseFeatureSystem("spe"))
        registry.register("pbase-uftc", PBaseFeatureSystem("uftc"))
    return registry


_DEFAULT_REGISTRY: Registry | None = None


def get_registry() -> Registry:
    """Return the lazily initialized default registry."""
    global _DEFAULT_REGISTRY  # noqa: PLW0603
    if _DEFAULT_REGISTRY is None:
        _DEFAULT_REGISTRY = create_registry()
    return _DEFAULT_REGISTRY


def set_registry(registry: Registry) -> None:
    """Replace the default registry."""
    global _DEFAULT_REGISTRY  # noqa: PLW0603
    _DEFAULT_REGISTRY = registry


def reset_registry() -> None:
    """Reset the default registry so it will be recreated lazily."""
    global _DEFAULT_REGISTRY  # noqa: PLW0603
    _DEFAULT_REGISTRY = None


def register(name: str, system: FeatureSystem) -> None:
    """Register a system in the default registry."""
    get_registry().register(name, system)


def get_system(name: str | None = None) -> FeatureSystem:
    """Get a system from the default registry."""
    return get_registry().get_system(name)


def list_systems() -> list[str]:
    """List systems from the default registry."""
    return get_registry().list_systems()


def set_default(name: str) -> None:
    """Set the default system in the default registry."""
    get_registry().set_default(name)


def get_features(grapheme: str, *, system: str | None = None) -> frozenset[str] | None:
    """Return features for a grapheme."""
    return get_system(system).grapheme_to_features(grapheme)


def get_representation(grapheme: str, *, system: str | None = None) -> FeatureRepresentation | None:
    """Return the native feature representation for a grapheme."""
    return get_system(system).grapheme_to_representation(grapheme)


def get_class_features(grapheme: str, *, system: str | None = None) -> frozenset[str] | None:
    """Return class features for a class symbol."""
    return get_system(system).class_features(grapheme)


def get_class_representation(
    grapheme: str,
    *,
    system: str | None = None,
) -> FeatureRepresentation | None:
    """Return the native representation for a class symbol."""
    return get_system(system).class_representation(grapheme)


def is_class(grapheme: str, *, system: str | None = None) -> bool:
    """Return whether the symbol is a class in the selected system."""
    return get_system(system).is_class(grapheme)


def features_to_grapheme(
    features: object,
    *,
    system: str | None = None,
) -> str | None:
    """Return a grapheme for the exact feature set."""
    return get_system(system).features_to_grapheme(features)


def add_features(
    base: frozenset[str],
    added: frozenset[str],
    *,
    system: str | None = None,
) -> frozenset[str]:
    """Add features using the selected system's semantics."""
    return get_system(system).add_features(base, added)


def partial_match(
    pattern: frozenset[str],
    target: frozenset[str],
    *,
    system: str | None = None,
) -> bool:
    """Check whether the pattern matches the target."""
    return get_system(system).partial_match(pattern, target)


def matches(
    pattern: object,
    target: object,
    *,
    system: str | None = None,
) -> bool:
    """Check whether the pattern matches the target using native semantics."""
    return get_system(system).matches(pattern, target)


def feature_distance(
    feat_a: str,
    feat_b: str,
    *,
    system: str | None = None,
) -> float:
    """Return the distance between two feature values."""
    return get_system(system).feature_distance(feat_a, feat_b)


def sound_distance(
    feats_a: frozenset[str],
    feats_b: frozenset[str],
    *,
    system: str | None = None,
) -> float:
    """Return the distance between two feature sets."""
    return get_system(system).sound_distance(feats_a, feats_b)


def segment_distance(
    a: object,
    b: object,
    *,
    system: str | None = None,
) -> float:
    """Return the distance between two native segment representations."""
    return get_system(system).segment_distance(a, b)
