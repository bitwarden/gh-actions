"""This is the entrypoint module for the workflow-linter CLI."""

import argparse
import sys

from typing import List, Optional

from .actions import ActionsCmd
from .lint import LinterCmd
from .utils import Settings


local_settings = Settings.factory()


def main(input_args: Optional[List[str]] = None) -> int:
    """CLI utility to lint GitHub Action Workflows.

    A CLI utility to enforce coding standards on GitHub Action workflows. The
    utility also provides other subcommands to assist with other workflow
    maintenance tasks; such as maintaining the list of approved GitHub Actions.
    """
    linter_cmd = LinterCmd(settings=local_settings)
    actions_cmd = ActionsCmd(settings=local_settings)

    # Read arguments from command line.
    parser = argparse.ArgumentParser(prog="bwwl")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    subparsers = parser.add_subparsers(required=True, dest="command")

    subparsers = LinterCmd.extend_parser(subparsers)
    subparsers = ActionsCmd.extend_parser(subparsers)

    # Pull the arguments from the command line
    input_args = sys.argv[1:]
    if not input_args:
        raise SystemExit(parser.print_help())

    args = parser.parse_args(input_args)

    if args.command == "lint":
        return linter_cmd.run(args.files, args.strict)

    if args.command == "actions":
        print(f"{'-'*50}\n!!bwwl actions is in BETA!!\n{'-'*50}")
        if args.actions_command == "add":
            return actions_cmd.add(args.name, args.output)
        if args.actions_command == "update":
            return actions_cmd.update(args.output)

    return -1


if __name__ == "__main__":
    sys.exit(main())
