import argparse
import os

from src.load import WorkflowBuilder, Rules
from src.utils import Colors, LintFinding, Settings, SettingsError


PROBLEM_LEVELS = {
    "warning": 1,
    "error": 2,
}


class LinterCmd:
    def __init__(self, settings: Settings = None, verbose: bool = True) -> None:
        self.rules = Rules(settings=settings, verbose=verbose)

    @staticmethod
    def extend_parser(subparsers: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """Extends the CLI subparser with the options for LintCmd.

        Add 'lint' as a sub command along with its options and arguments
        """
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
        return subparsers

    def get_max_error_level(self, findings: list[LintFinding]) -> int:
        """Get max error level from list of findings."""
        if len(findings) == 0:
            return 0
        max_problem = max(findings, key=lambda finding: PROBLEM_LEVELS[finding.level])
        max_problem_level = PROBLEM_LEVELS[max_problem.level]
        return max_problem_level

    def print_finding(self, finding: LintFinding) -> None:
        """Print formatted and colored finding."""
        if finding.level == "warning":
            color = Colors.yellow
        elif finding.level == "error":
            color = Colors.red
        else:
            color = Colors.white

        line = f"  - \033[{color}{finding.level}\033[0m {finding.description}"

        print(line)

    def lint_file(self, filename: str) -> int:
        findings = []
        max_error_level = 0

        print(f"Linting: {filename}\n")
        with open(filename) as file:
            workflow = WorkflowBuilder.build(filename)

            for rule in self.rules.workflow:
                findings.append(rule.execute(workflow))

            for job_key, job in workflow.jobs.items():
                for rule in self.rules.job:
                    findings.append(rule.execute(job))

                for step in job.steps:
                    for rule in self.rules.step:
                        findings.append(rule.execute(step))

        findings = list(filter(lambda a: a is not None, findings))

        if len(findings) > 0:
            for finding in findings:
                self.print_finding(finding)
            print()

        max_error_level = self.get_max_error_level(findings)

        return max_error_level

    def generate_files(self, files: list) -> list:
        """
        Takes in an argument of directory and/or files in list format from the CLI.
        Returns a sorted set of all workflow files in the path(s) specified.
        """
        workflow_files = []
        for path in files:
            if os.path.isfile(path):
                workflow_files.append(path)
            elif os.path.isdir(path):
                for subdir, dirs, files in os.walk(path):
                    for filename in files:
                        filepath = subdir + os.sep + filename
                        if filepath.endswith((".yml", ".yaml")):
                            workflow_files.append(filepath)

        return sorted(set(workflow_files))

    def run(self, input_files: list[str]) -> int:
        files = self.generate_files(input_files)

        if len(input_files) > 0:
            prob_levels = list(map(self.lint_file, files))

            max_error_level = max(prob_levels)

            if max_error_level == PROBLEM_LEVELS["error"]:
                return_code = 2
            elif max_error_level == PROBLEM_LEVELS["warning"]:
                return_code = 1 if args.strict else 0
            else:
                return_code = 0

            return return_code
        else:
            print(f'File(s)/Directory: "{input_files}" does not exist, exiting.')
            return -1
