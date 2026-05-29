# TODO
# - Update the 'description' value

import argparse
from boolbox.cli.commands import anf


def cli_main() -> int:
    parser = argparse.ArgumentParser(
        prog="boolbox", description="<I will change it later>"
    )

    # Parse sub-commands
    # Example: boolbox anf -> boolbox: main, anf: sub-command (generates anf polynomials)
    # Example: boolbox tts -> boolbox: main, tts: sub-command (generates  truth tables)
    #
    subparsers = parser.add_subparsers(dest="command", required=True, title="command")

    # Introduce the 'anf' sub-command to the boolbox
    #
    anf.register_parser(subparsers)

    # Parse arguments
    #
    args = parser.parse_args()

    # Dispatch
    #
    if args.command == "anf":
        return anf.run(args)

    # 0 = Success
    #
    return 0
