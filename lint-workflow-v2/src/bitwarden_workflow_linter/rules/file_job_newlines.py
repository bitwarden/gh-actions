"""A Rule to enforce newlines between each job."""

from typing import Union, Optional, Tuple, List

from ..models.file_format import FileFormat
from ..rule import Rule
from ..utils import LintLevels, Settings


class RuleFileJobNewline(Rule):
    """Rule to enforce specific prefixes for environment variables.

    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """RuleJobEnvironmentPrefix constructor to override the Rule class.

        Args:
          settings:
            A Settings object that contains any default, overridden, or custom settings
            required anywhere in the application.
        """
        self.message = "Missing empty newline between jobs"
        self.on_fail = LintLevels.ERROR
        self.compatibility = [FileFormat]
        self.settings = settings

    def fn(self, obj: FileFormat) -> Tuple[bool, str]:
        """Enforces a newline between every job block.

        Example:
        ---
        on:
          workflow_dispatch:

        jobs:
          first-job:
            runs-on: ubuntu-22.04
            steps:
              - run: echo test

          second-job:
            runs-on: ubuntu-22.04
            steps:
              - run: echo test

        There should be an empty newline between each job.
        """
        def get_block(lines: List[str]):
            block = []

            initial_length = len(lines[0])
            cleaned_length = len(lines[0].lstrip())
            initial_indent_size = initial_length - cleaned_length

            for index, line in enumerate(lines[1:]):
                if line[:initial_indent_size] != " " * initial_indent_size:
                    block = lines[:index]
                    break

            return block


        correct = True

        jobs_key_index = obj.lines.index("jobs:")
        jobs_blocks = obj.lines[jobs_key_index:]

        print(f"Blocks: {get_block(jobs_blocks)}")

        if correct:
            return True, ""

        return False, f"{self.message}"
