import sys
import argparse
import json

from boolbox.io.loaders import load_sbox
from boolbox.parser.sbox_parser import parse_sbox
from boolbox.core.mobius_transform import fmt


def register_parser(subparsers):
    """
    Registers the 'coeffs' command and its arguments to the main CLI parser

    Args:
        subparsers: The subparser object from argparse used to add new CLI commands
    """
    parser = subparsers.add_parser(
        "coeffs",
        help="Generate Möbius transform coefficients (ANF array) for an S-Box.",
    )

    parser.add_argument(
        "input", help="S-Box input. Can be '-', a file path, or a raw string."
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json", "latex"],
        default="text",
        help="Output format for the coefficients.",
    )


def run(args: argparse.Namespace) -> int:
    """
    Executes the 'coeffs' command logic
    Loads the S-Box, parses it into truth tables, applies the Fast Möbius Transform (FMT),
    and prints the formatted output

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
        truth_tables = parse_sbox(sbox_ints)
        coeffs_matrix = [fmt(tt) for tt in truth_tables]
    except Exception as e:
        print(f"Error generating Coefficients: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        output = {
            "metadata": {
                "type": "Mobius Coefficients",
                "bit_count": len(coeffs_matrix),
                "length": len(coeffs_matrix[0]) if coeffs_matrix else 0,
            },
            "coefficients": [
                {"bit_index": i, "coeff_array": array}
                for i, array in enumerate(coeffs_matrix)
            ],
        }
        print(json.dumps(output, indent=4))

    elif args.format == "text":
        for i, array in enumerate(coeffs_matrix):
            array_str = ", ".join(map(str, array))
            print(f"C_{i} = [{array_str}]")

    elif args.format == "latex":
        print("LaTeX formatting is not yet supported for this subcommand")

    return 0
