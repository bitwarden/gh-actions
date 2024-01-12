"""A Rule to enforce prefixes environment variables."""
from typing import Union, Tuple, List

from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..rule import Rule
from ..utils import LintLevels, Settings


class RuleJobEnvironmentPrefix(Rule):
    """Rule to enforce specific prefixes for environemnt variables.

    Automated testing is not easily written for GitHub Action Workflows. CI can also
    get complicated really quickly and take up hundreds of lines. All of this can
    make it very difficult to debug and troubleshoot, especially when environment
    variables can be set in four different places: Workflow level, Job level, Step
    level, and inside a shell Step.

    To alleviate some of the pain, we have decided that all Job level environment
    variables should be prefixed with an underscore. All Workflow environment
    variables are normally at the top of the file and Step level ones are pretty
    visible when debugging a shell Step.
    """
    def __init__(self, settings: Settings = None) -> None:
        """RuleJobEnvironmentPrefix constructor to override the Rule class.

        Args:
          settings:
            A Settings object that contains any default, overriden, or custom settings
            required anywhere in the application.
        """
        self.message: str = "Job environment vars should start with and underscore:"
        self.on_fail: LintLevels = LintLevels.ERROR
        self.compatibility: List[Union[Workflow, Job, Step]] = [Job]
        self.settings: Settings = settings

    def fn(self, obj: Job) -> Tuple[bool, str]:
        """Enforces the underscore prefix standard on job envs.

        Example:
        ---
        on:
          workflow_dispatch:

        jobs:
          job-key:
            runs-on: ubuntu-22.04
            env:
                _TEST_ENV: "test"
            steps:
              - run: echo test

        All keys under jobs.job-key.env should be prefixed with an underscore
        as in _TEST_ENV.

        See tests/rules/test_job_environment_prefix.py for examples of
        incorrectly names environment variables.
        """
        correct = True

        offending_keys = []
        for key in obj.env.keys():
            if key[0] != "_":
                offending_keys.append(key)
                correct = False

        if correct:
            return True, ""

        return False, f"{self.message} ({' ,'.join(offending_keys)})"
