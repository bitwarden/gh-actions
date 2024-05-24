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

        for index, line in enumerate(lines[jobs_key_index+1:]):
            if line == "" or line[0].isspace():
                block.append(line)
            else:
                break

        return block

    @classmethod
    def is_indentation_correct(cls, lines: List[str]) -> bool:
        jobs_key_index = lines.index("jobs:")

        for line in lines[jobs_key_index+1:]:
            if line == "":
                continue
            if line[2].isspace():
                return False

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

        print(f"blocks: {jobs_blocks}")


        #if correct:
        #    return True, ""

        return False, f"{self.message}"
