"""Phonological feature geometry tree (Clements & Hume 1995)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureNode:
    """Leaf: a binary phonological feature."""

    name: str
    positive: str
    negative: str


@dataclass(frozen=True)
class GeometryNode:
    """Internal node grouping features."""

    name: str
    children: tuple[GeometryNode | FeatureNode, ...]

    def all_features(self) -> frozenset[str]:
        """All leaf positive/negative values in this subtree."""
        result: set[str] = set()
        for child in self.children:
            if isinstance(child, FeatureNode):
                if child.positive:
                    result.add(child.positive)
                if child.negative:
                    result.add(child.negative)
            else:
                result |= child.all_features()
        return frozenset(result)

    def find_feature(self, value: str) -> FeatureNode | None:
        """Lookup a FeatureNode by positive or negative value."""
        for child in self.children:
            if isinstance(child, FeatureNode):
                if child.positive == value or child.negative == value:
                    return child
            else:
                result = child.find_feature(value)
                if result is not None:
                    return result
        return None

    def find_parent(self, value: str) -> GeometryNode | None:
        """Find the parent GeometryNode of a feature value."""
        for child in self.children:
            if isinstance(child, FeatureNode):
                if child.positive == value or child.negative == value:
                    return self
            elif isinstance(child, GeometryNode):
                for grandchild in child.children:
                    if isinstance(grandchild, FeatureNode) and (
                        grandchild.positive == value or grandchild.negative == value
                    ):
                        return child
                result = child.find_parent(value)
                if result is not None:
                    return result
        return None

    def siblings_of(self, value: str) -> frozenset[str]:
        """Sibling feature values under the same parent."""
        parent = self.find_parent(value)
        if parent is None:
            return frozenset()
        result: set[str] = set()
        for child in parent.children:
            if isinstance(child, FeatureNode):
                if child.positive and child.positive != value:
                    result.add(child.positive)
                if child.negative and child.negative != value:
                    result.add(child.negative)
        return frozenset(result)

    def _depth_of(self, value: str, depth: int = 0) -> int | None:
        """Find depth of a feature value in the tree."""
        for child in self.children:
            if isinstance(child, FeatureNode):
                if child.positive == value or child.negative == value:
                    return depth + 1
            else:
                result = child._depth_of(value, depth + 1)
                if result is not None:
                    return result
        return None

    def _path_to(self, value: str) -> list[str] | None:
        """Find path from root to a feature value (including the value itself)."""
        for child in self.children:
            if isinstance(child, FeatureNode):
                if child.positive == value or child.negative == value:
                    return [self.name, child.name, value]
            elif isinstance(child, GeometryNode):
                sub = child._path_to(value)
                if sub is not None:
                    return [self.name, *sub]
        return None

    def feature_distance(self, a: str, b: str) -> int:
        """Tree edge distance between two feature values."""
        if a == b:
            return 0
        path_a = self._path_to(a)
        path_b = self._path_to(b)
        if path_a is None or path_b is None:
            return 999
        common = 0
        for left, right in zip(path_a, path_b, strict=False):
            if left == right:
                common += 1
            else:
                break
        return (len(path_a) - common) + (len(path_b) - common)

    def sound_distance(self, feats_a: frozenset[str], feats_b: frozenset[str]) -> float:
        """Normalized distance between two feature sets using tree structure."""
        if feats_a == feats_b:
            return 0.0

        total_weight = 0.0
        total_diff = 0.0

        for leaf, depth in _iter_leaves(self, 1):
            weight = 1.0 / depth
            total_weight += weight

            a_has_pos = leaf.positive in feats_a if leaf.positive else False
            a_has_neg = leaf.negative in feats_a if leaf.negative else False
            b_has_pos = leaf.positive in feats_b if leaf.positive else False
            b_has_neg = leaf.negative in feats_b if leaf.negative else False

            if not (a_has_pos or a_has_neg or b_has_pos or b_has_neg):
                total_weight -= weight
                continue

            a_val = 1.0 if a_has_pos else (-1.0 if a_has_neg else 0.0)
            b_val = 1.0 if b_has_pos else (-1.0 if b_has_neg else 0.0)
            total_diff += weight * abs(a_val - b_val) / 2.0

        node_groups: dict[str, tuple[set[str], set[str]]] = {}
        for feat in feats_a | feats_b:
            node = FEATURE_TO_GEOMETRY_NODE.get(feat)
            if node is None:
                continue
            if node not in node_groups:
                node_groups[node] = (set(), set())
            if feat in feats_a:
                node_groups[node][0].add(feat)
            if feat in feats_b:
                node_groups[node][1].add(feat)

        for node_name, (a_set, b_set) in node_groups.items():
            depth = _node_depth(self, node_name, 1) or 2
            weight = 1.0 / depth
            total_weight += weight

            if a_set == b_set:
                continue
            if not a_set or not b_set:
                total_diff += weight * 0.5
            else:
                total_diff += weight

        return total_diff / total_weight if total_weight > 0 else 0.0


def _iter_leaves(node: GeometryNode, depth: int) -> list[tuple[FeatureNode, int]]:
    """Iterate over all leaf FeatureNodes with their depth."""
    result: list[tuple[FeatureNode, int]] = []
    for child in node.children:
        if isinstance(child, FeatureNode):
            result.append((child, depth))
        else:
            result.extend(_iter_leaves(child, depth + 1))
    return result


def _node_depth(root: GeometryNode, name: str, depth: int) -> int | None:
    """Find the depth of a named GeometryNode in the tree."""
    if root.name == name:
        return depth
    for child in root.children:
        if isinstance(child, GeometryNode):
            result = _node_depth(child, name, depth + 1)
            if result is not None:
                return result
    return None


DEFAULT_GEOMETRY = GeometryNode(
    name="Root",
    children=(
        GeometryNode(
            name="Laryngeal",
            children=(
                FeatureNode(name="voice", positive="voiced", negative="voiceless"),
                FeatureNode(name="spread_glottis", positive="aspirated", negative=""),
                FeatureNode(name="constricted_glottis", positive="glottalized", negative=""),
                FeatureNode(name="breathy_voice", positive="breathy", negative=""),
                FeatureNode(name="creaky_voice", positive="creaky", negative=""),
            ),
        ),
        GeometryNode(
            name="Manner",
            children=(
                FeatureNode(name="sonorant", positive="sonorant", negative="obstruent"),
                FeatureNode(name="continuant", positive="continuant", negative=""),
                FeatureNode(name="nasal", positive="nasal", negative=""),
                FeatureNode(name="lateral", positive="lateral", negative=""),
                FeatureNode(name="strident", positive="sibilant", negative=""),
                FeatureNode(name="delayed_release", positive="affricate", negative=""),
                FeatureNode(name="tap_feature", positive="tap", negative=""),
                FeatureNode(name="syllabic", positive="syllabic", negative="non-syllabic"),
            ),
        ),
        GeometryNode(
            name="Place",
            children=(
                GeometryNode(
                    name="Labial",
                    children=(FeatureNode(name="round", positive="rounded", negative="unrounded"),),
                ),
                GeometryNode(
                    name="Coronal",
                    children=(
                        FeatureNode(name="anterior", positive="anterior", negative=""),
                        FeatureNode(name="distributed", positive="distributed", negative=""),
                    ),
                ),
                GeometryNode(
                    name="Dorsal",
                    children=(
                        FeatureNode(name="high", positive="close", negative="open"),
                        FeatureNode(name="low", positive="near-open", negative="near-close"),
                        FeatureNode(name="back", positive="back", negative="front"),
                    ),
                ),
                GeometryNode(
                    name="Pharyngeal",
                    children=(
                        FeatureNode(name="pharyngeal_place", positive="pharyngeal", negative=""),
                        FeatureNode(name="epiglottal_place", positive="epiglottal", negative=""),
                    ),
                ),
                GeometryNode(
                    name="Glottal",
                    children=(FeatureNode(name="glottal_place", positive="glottal", negative=""),),
                ),
            ),
        ),
        GeometryNode(
            name="TongueRoot",
            children=(
                FeatureNode(
                    name="atr",
                    positive="advanced-tongue-root",
                    negative="retracted-tongue-root",
                ),
            ),
        ),
        GeometryNode(
            name="Prosodic",
            children=(
                FeatureNode(name="long_feature", positive="long", negative=""),
                FeatureNode(name="nasalized_feature", positive="nasalized", negative=""),
                FeatureNode(name="labialized_feature", positive="labialized", negative=""),
                FeatureNode(name="palatalized_feature", positive="palatalized", negative=""),
                FeatureNode(name="pharyngealized_feature", positive="pharyngealized", negative=""),
                FeatureNode(name="ejective_feature", positive="ejective", negative=""),
                FeatureNode(name="stress_feature", positive="primary-stress", negative=""),
            ),
        ),
    ),
)

FEATURE_TO_GEOMETRY_NODE: dict[str, str] = {
    "voiced": "Laryngeal",
    "voiceless": "Laryngeal",
    "aspirated": "Laryngeal",
    "glottalized": "Laryngeal",
    "breathy": "Laryngeal",
    "creaky": "Laryngeal",
    "stop": "Manner",
    "fricative": "Manner",
    "affricate": "Manner",
    "nasal": "Manner",
    "approximant": "Manner",
    "trill": "Manner",
    "tap": "Manner",
    "lateral": "Manner",
    "click": "Manner",
    "implosive": "Manner",
    "sibilant": "Manner",
    "syllabic": "Manner",
    "non-syllabic": "Manner",
    "bilabial": "Labial",
    "labio-dental": "Labial",
    "labio-velar": "Labial",
    "labio-palatal": "Labial",
    "labial": "Labial",
    "rounded": "Labial",
    "unrounded": "Labial",
    "dental": "Coronal",
    "alveolar": "Coronal",
    "post-alveolar": "Coronal",
    "alveolo-palatal": "Coronal",
    "retroflex": "Coronal",
    "linguolabial": "Coronal",
    "palatal": "Dorsal",
    "palatal-velar": "Dorsal",
    "velar": "Dorsal",
    "uvular": "Dorsal",
    "close": "Dorsal",
    "near-close": "Dorsal",
    "close-mid": "Dorsal",
    "mid": "Dorsal",
    "open-mid": "Dorsal",
    "near-open": "Dorsal",
    "open": "Dorsal",
    "front": "Dorsal",
    "near-front": "Dorsal",
    "central": "Dorsal",
    "near-back": "Dorsal",
    "back": "Dorsal",
    "pharyngeal": "Pharyngeal",
    "epiglottal": "Pharyngeal",
    "glottal": "Glottal",
    "advanced-tongue-root": "TongueRoot",
    "retracted-tongue-root": "TongueRoot",
    "long": "Prosodic",
    "nasalized": "Prosodic",
    "labialized": "Prosodic",
    "palatalized": "Prosodic",
    "pharyngealized": "Prosodic",
    "ejective": "Prosodic",
    "primary-stress": "Prosodic",
}
