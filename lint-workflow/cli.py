import sys
import argparse
import os
import yaml
import json

# from src.rules import workflow_rules, job_rules, step_rules, uses_step_rules, run_step_rules
import settings
from src.actions import Actions
from src.utils import Settings, SettingsError
from src.lint import Linter


try:
    lint_settings = Settings(
        enabled_rules=settings.enabled_rules, approved_actions=settings.approved_actions
    )
except:
    raise SettingsError(
        (
            "Required settings: enabled_rules, approved_actions\n"
            "Please see documentation for more information"
        )
    )

linter = Linter(settings=lint_settings)
actions = Actions(settings=lint_settings)

# print(lint_rules.workflow)


def main(input_args=None):
    # Read arguments from command line.
    parser = argparse.ArgumentParser(prog="workflow-linter")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    subparsers = parser.add_subparsers(required=True, dest="command")

    parser_actions = subparsers.add_parser("actions", help="actions help")
    parser_actions.add_argument(
        "-o", "--output", action="store", default="actions.json"
    )
    subparsers_actions = parser_actions.add_subparsers(
        required=True, dest="actions_command"
    )

    parser_actions_update = subparsers_actions.add_parser(
        "update", help="update action versions"
    )

    parser_actions_add = subparsers_actions.add_parser(
        "add", help="add action to approved list"
    )
    parser_actions_add.add_argument("name", help="action name [git owener/repo]")

    parser_lint = subparsers.add_parser("lint", help="lint help")
    parser_lint.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="return non-zero exit code on warnings as well as errors",
    )
    parser_lint.add_argument("-f", "--files", action="append", help="files to lint")
    parser_lint.add_argument(
        "--output",
        action="store",
        help="output format: [stdout|json|md]",
        default="stdout",
    )

    # Pull the arguments from the command line
    input_args = sys.argv[1:]
    if not input_args:
        raise SystemExit(parser.print_help())

    args = parser.parse_args(input_args)

    if args.verbose:
        print(f"Args:\n{args}")

    if args.command == "lint":
        return linter.run(args.files)

    if args.command == "actions":
        if args.actions_command == "add":
            return actions.add(args.name, args.output)
        elif args.actions_command == "update":
            return actions.update(args.output)
        return -1


if __name__ == "__main__":
    return_code = main()
    # print(memoized_action_update_urls)
    sys.exit(return_code)
