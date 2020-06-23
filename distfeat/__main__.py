#!/usr/bin/env python3

"""
__main__.py

Module for command-line execution.
"""

# TODO: add grapheme2features options

# Import Python standard libraries
import argparse
import sys

# Import our library
import distfeat


def parse_arguments():
    # Create top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")

    # Create the parser for the "query" command
    parser_query = subparsers.add_parser("query", help="Query the feature database")
    parser_query.add_argument("grapheme", type=str, help="Grapheme to query")
    parser_query.set_defaults(command="query")

    # Create the parser for the "train" command
    parser_distance = subparsers.add_parser(
        "distance", help="Compute the distance between two graphemes"
    )
    parser_distance.add_argument(
        "grapheme_a", type=str, help="First grapheme for distance quantification"
    )
    parser_distance.add_argument(
        "grapheme_b", type=str, help="Second grapheme for distance quantification"
    )
    parser_distance.set_defaults(command="distance")

    args = parser.parse_args()

    return args


def main():
    """
    Main function for DistFeat call from command line.
    """

    # Get arguments
    args = parse_arguments()

    # Act accordingly
    df = distfeat.DistFeat()
    try:
        if args.command == "query":
            print(df.grapheme2features(args.grapheme))
        elif args.command == "distance":
            print(df.distance(args.grapheme_a, args.grapheme_b))
    except AttributeError:
        print("distfeat: error, must provide a command")


if __name__ == "__main__":
    main()
