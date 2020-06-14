#!/usr/bin/env python3

"""
test_distfeat
=============

Tests for the `distfeat` package.
"""

# Import Python libraries
import sys
import unittest

# Import the library itself
import distfeat


class TestDistFeat(unittest.TestCase):
    # Build main DistFeat object
    df = distfeat.DistFeat()

    def test_grapheme2features(self):
        # Obtain vectors with and without truth values
        v1 = self.df.grapheme2features("a")
        v2 = self.df.grapheme2features("a", t_values=False)

        # Build comparable values
        v1_tuple = tuple(v1.items())
        v2_tuple = tuple(v2.items())

        # Assert values
        assert v1_tuple == (
            ("anterior", True),
            ("approximant", True),
            ("back", False),
            ("click", False),
            ("consonantal", False),
            ("constricted", False),
            ("continuant", True),
            ("coronal", True),
            ("distributed", True),
            ("dorsal", True),
            ("high", False),
            ("labial", False),
            ("laryngeal", True),
            ("lateral", False),
            ("long", None),
            ("low", True),
            ("nasal", False),
            ("pharyngeal", None),
            ("place", True),
            ("preaspirated", None),
            ("preglottalized", None),
            ("prenasal", None),
            ("round", None),
            ("sibilant", False),
            ("sonorant", True),
            ("spread", False),
            ("strident", False),
            ("syllabic", True),
            ("tense", True),
            ("voice", True),
        )
        assert v2_tuple == (
            ("anterior", "+"),
            ("approximant", "+"),
            ("back", "-"),
            ("click", "-"),
            ("consonantal", "-"),
            ("constricted", "-"),
            ("continuant", "+"),
            ("coronal", "+"),
            ("distributed", "+"),
            ("dorsal", "+"),
            ("high", "-"),
            ("labial", "-"),
            ("laryngeal", "+"),
            ("lateral", "-"),
            ("long", "0"),
            ("low", "+"),
            ("nasal", "-"),
            ("pharyngeal", "0"),
            ("place", "+"),
            ("preaspirated", "0"),
            ("preglottalized", "0"),
            ("prenasal", "0"),
            ("round", "0"),
            ("sibilant", "-"),
            ("sonorant", "+"),
            ("spread", "-"),
            ("strident", "-"),
            ("syllabic", "+"),
            ("tense", "+"),
            ("voice", "+"),
        )

    def test_features2graphemes(self):
        # Obtain lists
        l1 = self.df.features2graphemes(
            {"consonantal": "-", "anterior": "+", "high": "-", "long": "+"}
        )
        l2 = self.df.features2graphemes(
            {"consonantal": False, "anterior": True, "high": False, "long": True},
            t_values=True,
        )
        l3 = self.df.features2graphemes(
            {"consonantal": "-", "anterior": "+", "high": "-"}, drop_na=True
        )

        # Build comparable values
        l1_tuple = tuple(l1)
        l2_tuple = tuple(l2)
        l3_tuple = tuple(l3)

        # Assert values
        assert l1_tuple == (
            "aː",
            "ãː",
            "eː",
            "ẽː",
            "æː",
            "æ̃ː",
            "øː",
            "ø̃ː",
            "œː",
            "œ̃ː",
            "ɶː",
            "ɶ̃ː",
        )
        assert l1_tuple == l2_tuple
        assert l3_tuple == (
            "a",
            "aː",
            "ã",
            "ãː",
            "ă",
            "ḁ",
            "a̯",
            "e",
            "eː",
            "ẽ",
            "ẽː",
            "ĕ",
            "e̤",
            "e̥",
            "e̯",
            "æ",
            "æː",
            "æ̃",
            "æ̃ː",
            "ø",
            "øː",
            "ø̃",
            "ø̃ː",
            "œ",
            "œː",
            "œ̃",
            "œ̃ː",
            "ɶ",
            "ɶː",
            "ɶ̃",
            "ɶ̃ː",
        )

    def test_minimal_matrix(self):
        # Obtain matrix dictionaries
        m1 = self.df.minimal_matrix(["t", "f", "s"])
        m2 = self.df.minimal_matrix(["t", "f", "s"], drop_na=True)
        m3 = self.df.minimal_matrix(["t", "f", "s"], t_values=False)

        # Build comparable values
        m1_tuple = tuple(m1.items())
        m2_tuple = tuple(m2.items())
        m3_tuple = tuple(m3.items())

        # Assert values
        assert m1_tuple == (
            (
                "f",
                {
                    "continuant": True,
                    "distributed": True,
                    "labial": True,
                    "round": False,
                    "sibilant": False,
                    "strident": True,
                },
            ),
            (
                "s",
                {
                    "continuant": True,
                    "distributed": False,
                    "labial": False,
                    "round": None,
                    "sibilant": True,
                    "strident": True,
                },
            ),
            (
                "t",
                {
                    "continuant": False,
                    "distributed": False,
                    "labial": False,
                    "round": None,
                    "sibilant": False,
                    "strident": False,
                },
            ),
        )
        assert m2_tuple == (
            (
                "f",
                {
                    "continuant": True,
                    "distributed": True,
                    "labial": True,
                    "sibilant": False,
                    "strident": True,
                },
            ),
            (
                "s",
                {
                    "continuant": True,
                    "distributed": False,
                    "labial": False,
                    "sibilant": True,
                    "strident": True,
                },
            ),
            (
                "t",
                {
                    "continuant": False,
                    "distributed": False,
                    "labial": False,
                    "sibilant": False,
                    "strident": False,
                },
            ),
        )
        assert m3_tuple == (
            (
                "f",
                {
                    "continuant": "+",
                    "distributed": "+",
                    "labial": "+",
                    "round": "-",
                    "sibilant": "-",
                    "strident": "+",
                },
            ),
            (
                "s",
                {
                    "continuant": "+",
                    "distributed": "-",
                    "labial": "-",
                    "round": "0",
                    "sibilant": "+",
                    "strident": "+",
                },
            ),
            (
                "t",
                {
                    "continuant": "-",
                    "distributed": "-",
                    "labial": "-",
                    "round": "0",
                    "sibilant": "-",
                    "strident": "-",
                },
            ),
        )

    def test_class_features(self):
        # Obtain class feature dictionaries
        cf1 = self.df.class_features(["t", "f", "s"])
        cf2 = self.df.class_features(["t", "f", "s"], drop_na=True)
        cf3 = self.df.class_features(["t", "f", "s"], t_values=False)

        # Build comparable values
        cf1_tuple = tuple(cf1.items())
        cf2_tuple = tuple(cf2.items())
        cf3_tuple = tuple(cf3.items())

        # Assert values
        assert cf1_tuple == (
            ("anterior", True),
            ("approximant", False),
            ("click", False),
            ("consonantal", True),
            ("coronal", True),
            ("dorsal", False),
            ("laryngeal", False),
            ("lateral", False),
            ("nasal", False),
            ("place", True),
            ("round", False),
            ("sonorant", False),
            ("syllabic", False),
            ("tense", False),
        )
        assert cf2_tuple == (
            ("anterior", True),
            ("approximant", False),
            ("click", False),
            ("consonantal", True),
            ("coronal", True),
            ("dorsal", False),
            ("laryngeal", False),
            ("lateral", False),
            ("nasal", False),
            ("place", True),
            ("round", False),
            ("sonorant", False),
            ("syllabic", False),
            ("tense", False),
        )
        assert cf3_tuple == (
            ("anterior", "+"),
            ("approximant", "-"),
            ("click", "-"),
            ("consonantal", "+"),
            ("coronal", "+"),
            ("dorsal", "-"),
            ("laryngeal", "-"),
            ("lateral", "-"),
            ("nasal", "-"),
            ("place", "+"),
            ("round", "-"),
            ("sonorant", "-"),
            ("syllabic", "-"),
            ("tense", "-"),
        )


if __name__ == "__main__":
    # explicitly creating and running a test suite allows to profile
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDistFeat)
    unittest.TextTestRunner(verbosity=2).run(suite)
