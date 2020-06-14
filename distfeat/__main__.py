#!/usr/bin/env python3

"""
__main__.py

Module for command-line execution.
"""

# Import Python standard libraries
import argparse
import sys

# Import our library
import distfeat


def main():
    """
    Main function for DistFeat call from command line.
    """

    if len(sys.argv) != 2:
        print("DistFeat auxiliary query tool")
        print("Usage: distfeat grapheme")
        return

    # build object
    df = distfeat.DistFeat()

    # print grapheme vector
    print(df.grapheme2features(sys.argv[1]))


if __name__ == "__main__":
    main()
