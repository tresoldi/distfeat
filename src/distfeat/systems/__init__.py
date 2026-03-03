"""Built-in feature-system implementations."""

from distfeat.systems.categorical import CategoricalFeatureSystem
from distfeat.systems.distinctive import DistinctiveFeatureSystem
from distfeat.systems.ipa import IPAFeatureSystem
from distfeat.systems.pbase import PBaseFeatureSystem
from distfeat.systems.tresoldi import TresoldiFeatureSystem

__all__ = [
    "CategoricalFeatureSystem",
    "DistinctiveFeatureSystem",
    "IPAFeatureSystem",
    "PBaseFeatureSystem",
    "TresoldiFeatureSystem",
]
