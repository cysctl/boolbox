import argparse

# Sub-commands
#
from boolbox.cli.commands import anf
from boolbox.cli.commands import tts
from boolbox.cli.commands import coeffs


def cli_main() -> int:
    parser = argparse.ArgumentParser(
        prog="boolbox", description="A lightweight cryptographic Boolean function analysis tool."
    )

    # Parse sub-commands
    # Example: boolbox anf -> boolbox: main, anf: sub-command (generates anf polynomials)
    # Example: boolbox tts -> boolbox: main, tts: sub-command (generates  truth tables)
    #
    subparsers = parser.add_subparsers(dest="command", required=True, title="command")

    # Introduce the sub-commands to the boolbox
    #
    anf.register_parser(subparsers)
    tts.register_parser(subparsers)
    coeffs.register_parser(subparsers)

    # Parse arguments
    #
    args = parser.parse_args()

    # Dispatch
    #
    if args.command == "anf":
        return anf.run(args)
    elif args.command == "tts":
        return tts.run(args)
    elif args.command == "coeffs":
        return coeffs.run(args)

    # 0 = Success
    #
    return 0
