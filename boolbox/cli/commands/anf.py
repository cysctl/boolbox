import sys
import argparse
from boolbox.pipeline import sbox_to_poly
from boolbox.formatters.text import TextFormatter
from boolbox.formatters.latex import LaTeXFormatter
from boolbox.formatters.json import JSONFormatter
from boolbox.formatters.unicode import UnicodeFormatter
from boolbox.io.loaders import load_sbox


def register_parser(subparsers):
    """
    Registers the 'anf' command and its arguments to the main CLI parser

    Args:
        subparsers: The subparser object from argparse used to add new CLI commands
    """

    parser = subparsers.add_parser(
        "anf", help="Convert an S-Box to Algebraic Normal Form (ANF) polynomials."
    )

    parser.add_argument(
        "input",
        help="S-Box input. Can be '-', a file path, or a raw string like '[0xC, 0x5]' or '12, 5'.",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "latex", "json", "unicode"],
        default="text",
        help="Output format for the generated polynomials.",
    )


def run(args: argparse.Namespace) -> int:
    """
    Executes the 'anf' command logic
    Loads the S-Box, processes it through the pipeline, and prints the formatted output

    Args:
        args: The parsed command-line arguments containing user inputs

    Returns:
        An integer representing the system exit status code (0 = success, 1 = error)
    """

    # Parse input
    #
    try:
        sbox_ints = load_sbox(args.input)
    except Exception as e:
        print(f"Error loading S-Box: {e}", file=sys.stderr)
        return 1

    # Run pipeline
    #
    try:
        polys = sbox_to_poly(sbox_ints)
    except Exception as e:
        print(f"Error processing S-Box: {e}", file=sys.stderr)
        return 1

    # Select formatter
    #
    if args.format == "text":
        formatter = TextFormatter()
    elif args.format == "latex":
        formatter = LaTeXFormatter()
    elif args.format == "json":
        formatter = JSONFormatter()
    elif args.format == "unicode":
        formatter = UnicodeFormatter()

    # Print result
    #
    print(formatter.format(polys))

    return 0
