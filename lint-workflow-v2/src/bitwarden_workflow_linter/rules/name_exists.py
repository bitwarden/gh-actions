"""A Rule to enforce that a 'name' key exists."""

from typing import Optional, Tuple, Union

from ..models.workflow import Workflow
from ..models.job import Job
from ..models.step import Step
from ..rule import Rule
from ..utils import LintLevels, Settings


class RuleNameExists(Rule):
    """Rule to enforce a 'name' key exists for every object in GitHub Actions.

    For pipeline run troubleshooting and debugging, it is helpful to have a
    name to immediately identify a Workflow, Job, or Step while moving between
    run and the code.

    It also helps with uniformity of runs.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Constructor for RuleNameCapitalized to override Rule class.

        Args:
          settings:
            A Settings object that contains any default, overridden, or custom settings
            required anywhere in the application.
        """
        self.message = "name must exist"
        self.on_fail = LintLevels.ERROR
        self.settings = settings

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
