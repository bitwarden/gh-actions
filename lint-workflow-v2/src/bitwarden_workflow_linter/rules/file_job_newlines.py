"""A Rule to enforce newlines between each job."""

from typing import Union, Optional, Tuple, List

from ..models.file_format import FileFormat
from ..rule import Rule
from ..utils import LintLevels, Settings


INDENTATION_LEVEL = 2

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

    @classmethod
    def get_job_blocks(cls, lines: List[str]) -> List[str]:
        jobs_key_index = lines.index("jobs:")
        block = []

        for line in lines[jobs_key_index+1:]:
            if line == "" or line[0].isspace():
                block.append(line)
            else:
                break

        return block

    @classmethod
    def is_start_new_job_block(cls, line: str) -> bool:
        return not line[2].isspace()

    @classmethod
    def is_indentation_correct(cls, lines: List[str]) -> bool:
        jobs_key_index = lines.index("jobs:")

        for line in lines[jobs_key_index+1:]:
            print(f"indentation check line: {line}")
            if line == "":
                continue
            if not cls.is_start_new_job_block(line):
                return False
            else:
                return True

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

        There should be an empty newline between each job. This assumes and validates a YAML
        indentiation of INDENTATION_LEVEL.
        """
        correct = True

        if not self.is_indentation_correct(obj.lines):
            return False, f"Dependent YAML indentation is incorrect. Required: {INDENTATION_LEVEL}"

        jobs_blocks = self.get_job_blocks(obj.lines)

        if job_block[0] == "":
            return False, f"There should be no newline between the 'jobs' key and the first job"

        for index, line in enumerate(jobs_block):
            if index == 0: # skip the first job
                continue
            if self.is_start_new_job_block(line) and jobs_blocks[index-1] != "":
                self.message += f"\nMissing newline prior to {jobs_blocks[index]}"
                correct = False

        if correct:
            return True, ""

        return False, f"{self.message}"
