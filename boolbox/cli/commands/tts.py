import sys
import argparse
import json

from boolbox.io.loaders import load_sbox
from boolbox.parser.sbox_parser import parse_sbox


def register_parser(subparsers):
    """
    Registers the 'tts' command and its arguments to the main CLI parser

    Args:
        subparsers: The subparser object from argparse used to add new CLI commands
    """

    parser = subparsers.add_parser(
        "tts", help="Generate Truth Tables for each bit of an S-Box."
    )

    parser.add_argument(
        "input", help="S-Box input. Can be '-', a file path, or a raw string."
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json", "latex"],
        default="text",
        help="Output format for the truth tables.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """
    Executes the 'tts' command logic
    Loads the S-Box, generates the Truth Tables using the parser, and prints the formatted output

    Args:
        args: The parsed command-line arguments containing user inputs

    Returns:
        An integer representing the system exit status code (0 = success, 1 = error)
    """

    try:
        sbox_ints = load_sbox(args.input)
    except Exception as e:
        print(f"Error loading S-Box: {e}", file=sys.stderr)
        return 1

    try:
        tts = parse_sbox(sbox_ints)
    except Exception as e:
        print(f"Error generating truth tables: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        # Generate a JSON object
        #
        output = {
            "metadata": {
                "type": "Truth Tables",
                "bit_count": len(tts),
                "length": len(tts[0]) if tts else 0,
            },
            "tables": [
                {"bit_index": i, "truth_table": table} for i, table in enumerate(tts)
            ],
        }

        # JSON string
        #
        print(json.dumps(output, indent=4))

    elif args.format == "text":
        for i, table in enumerate(tts):
            table_str = ", ".join(map(str, table))
            print(f"S_{i} = [{table_str}]")

    elif args.format == "latex":
        print("LaTeX formatting is not yet supported for this subcommand")

    return 0
