"""Module providing Lint subcommand to run custom linting rules against GitHub Action
Workflows."""

import argparse
import os

from functools import reduce
from typing import Optional

from .load import WorkflowBuilder, Rules
from .utils import LintFinding, Settings


class LinterCmd:
    """Command to lint GitHub Action Workflow files

    This class contains logic to lint workflows that are passed in.
    Supporting logic is supplied to:
      - build out the list of Rules desired
      - select and validate the workflow files to lint
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Initailize the LinterCmd class.

        Args:
          settings:
            A Settings object that contains any default, overridden, or custom settings
            required anywhere in the application.
        """
        self.rules = Rules(settings=settings)

    @staticmethod
    def extend_parser(
        subparsers: argparse._SubParsersAction,
    ) -> argparse._SubParsersAction:
        """Extends the CLI subparser with the options for LintCmd.

        Add 'lint' as a subcommand along with its options and arguments

        Args:
          subparsers:
            The main argument parser to add subcommands and arguments to
        """
        parser_lint = subparsers.add_parser(
            "lint",
            help="Verify that a GitHub Action Workflow follows all of the Rules.",
        )
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
        return subparsers

    def get_max_error_level(self, findings: list[LintFinding]) -> int:
        """Get max error level from list of findings.

        Compute the maximum error level to determine the exit code required.
        # if max(error) return exit(1); else return exit(0)

        Args:
          findings:
            All of the findings that the linter found while linting a workflow.

        Return:
          The numeric value of the maximum lint finding
        """
        if len(findings) == 0:
            return 0
        return max(findings, key=lambda finding: finding.level.code).level.code

    def lint_file(self, filename: str) -> int:
        """Lint a single workflow.

        Run all of the Workflow, Job, and Step level rules that have been enabled.

        Args:
          filename:
            The name of the file that contains the workflow to lint

        Returns:
          The maximum error level found in the file (none, warning, error) to
          calculate the exit code from.
        """
        findings = []
        max_error_level = 0

        print(f"Linting: {filename}")
        workflow = WorkflowBuilder.build(filename)

        for rule in self.rules.workflow:
            findings.append(rule.execute(workflow))

        for _, job in workflow.jobs.items():
            for rule in self.rules.job:
                findings.append(rule.execute(job))

            if job.steps is not None:
                for step in job.steps:
                    for rule in self.rules.step:
                        findings.append(rule.execute(step))

        findings = list(filter(lambda a: a is not None, findings))

        if len(findings) > 0:
            for finding in findings:
                print(f" - {finding}")
            print()

        max_error_level = self.get_max_error_level(findings)

        return max_error_level

    def generate_files(self, files: list[str]) -> list[str]:
        """Generate the list of files to lint.

        Searches the list of directory and/or files taken from the CLI.

        Args:
          files:
            list of file names or directory names.

        Returns:
          A sorted set of all workflow files in the path(s) specified.
        """
        workflow_files = []
        for path in files:
            if os.path.isfile(path):
                workflow_files.append(path)
            elif os.path.isdir(path):
                for subdir, _, files in os.walk(path):
                    for filename in files:
                        filepath = subdir + os.sep + filename
                        if filepath.endswith((".yml", ".yaml")):
                            workflow_files.append(filepath)

        return sorted(set(workflow_files))

    def run(self, input_files: list[str], strict: bool = False) -> int:
        """Execute the LinterCmd.

        Args:
          input_files:
            list of file names or directory names.
          strict:
            fail on WARNING instead of succeed

        Returns
          The return_code for the entire CLI to indicate success/failure
        """
        files = self.generate_files(input_files)

        if len(input_files) > 0:
            return_code = reduce(
                lambda a, b: a if a > b else b, map(self.lint_file, files)
            )

            if return_code == 1 and not strict:
                return_code = 0

            return return_code
        else:
            print(f'File(s)/Directory: "{input_files}" does not exist, exiting.')
            return -1
