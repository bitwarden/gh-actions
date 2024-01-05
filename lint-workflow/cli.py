import sys
import argparse
import os
import yaml
import json

# from src.rules import workflow_rules, job_rules, step_rules, uses_step_rules, run_step_rules
import settings
from src.actions import ActionsCmd
from src.utils import Settings, SettingsError
from src.lint import LinterCmd


try:
    local_settings = Settings(
        enabled_rules=settings.enabled_rules, approved_actions=settings.approved_actions
    )
except:
    raise SettingsError(
        (
            "Required settings: enabled_rules, approved_actions\n"
            "Please see documentation for more information"
        )
    )


def main(input_args=None):
    """CLI utility to lint GitHub Action Workflows.

    A CLI utility to enforce coding standards on GitHub Action workflows. The
    utility also provides other sub-commands to assist with other workflow
    maintenance tasks; such as maintaining the list of approved GitHub Actions.
    """
    linter_cmd = LinterCmd(settings=local_settings)
    actions_cmd = ActionsCmd(settings=local_settings)

    # Read arguments from command line.
    parser = argparse.ArgumentParser(prog="workflow-linter")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    subparsers = parser.add_subparsers(required=True, dest="command")

    subparsers = LinterCmd.extend_parser(subparsers)
    subparsers = ActionsCmd.extend_parser(subparsers)

    # Pull the arguments from the command line
    input_args = sys.argv[1:]
    if not input_args:
        raise SystemExit(parser.print_help())

    args = parser.parse_args(input_args)

    if args.verbose:
        print(f"Args:\n{args}")

    if args.command == "lint":
        return linter_cmd.run(args.files)

    if args.command == "actions":
        if args.actions_command == "add":
            return actions_cmd.add(args.name, args.output)
        elif args.actions_command == "update":
            return actions_cmd.update(args.output)
        return -1


if __name__ == "__main__":
    return_code = main()
    sys.exit(return_code)
