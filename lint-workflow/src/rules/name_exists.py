from typing import Union, Tuple

from ..rule import Rule
from ..models.workflow import Workflow
from ..models.job import Job
from ..models.step import Step
from ..utils import LintLevels, Settings


class RuleNameExists(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = "name must exist"
        self.on_fail: LintLevels = LintLevels.ERROR
        self.settings: Settings = settings

    def fn(self, obj: Union[Workflow, Job, Step]) -> Tuple[bool, str]:
        """Enforces the existence of names.

        Example:
        ---
        name: Test Workflow

        on:
          workflow_dispatch:

        jobs:
          job-key:
            name: Test
            runs-on: ubuntu-latest
            steps:
              - name: Test
                run: echo test

        'Test Workflow', 'Test', and 'Test' all exist.

        See tests/rules/test_name_exists.py for examples where a name does not
        exist.
        """
        if obj.name is not None:
            return True, ""
        return False, self.message
