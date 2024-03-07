"""A Rule to enforce all 'name' values start with a capital letter."""

from typing import Optional, Tuple, Union

from ..models.job import Job
from ..models.step import Step
from ..models.workflow import Workflow
from ..rule import Rule
from ..utils import LintLevels, Settings


class RuleNameCapitalized(Rule):
    """Rule to enforce all 'name' values start with a capital letter.

    A simple standard to help keep uniformity in naming.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Constructor for RuleNameCapitalized to override the Rule class.

        Args:
          settings:
            A Settings object that contains any default, overridden, or custom settings
            required anywhere in the application.
        """
        self.message = "name must capitalized"
        self.on_fail = LintLevels.ERROR
        self.settings = settings

    def fn(self, obj: Union[Workflow, Job, Step]) -> Tuple[bool, str]:
        """Enforces capitalization of the first letter of any name key.

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

        'Test Workflow', 'Test', and 'Test' all start with a capital letter.

        See tests/rules/test_name_capitalized.py for examples of incorrectly
        capitalized names. This Rule DOES NOT enforce that the name exists.
        It only enforces capitalization IF it does.
        """
        if obj.name:
            return obj.name[0].isupper(), self.message
        return True, ""  # Force passing if obj.name doesn't exist
