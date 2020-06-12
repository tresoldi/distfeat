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
    def test_dummy(self):
        """
        Dummy test.
        """

        assert 2 + 2 == 4


if __name__ == "__main__":
    # explicitly creating and running a test suite allows to profile
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDistFeat)
    unittest.TextTestRunner(verbosity=2).run(suite)
