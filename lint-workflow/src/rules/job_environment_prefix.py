from typing import Union, Tuple

from ..rule import Rule
from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..utils import LintLevels, Settings


class RuleJobEnvironmentPrefix(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message: str = f"Job Environment vars should start with and underscore:"
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
        for key, value in obj.env.items():
            if key[0] != "_":
                offending_keys.append(key)
                correct = False

        if correct:
            return True, ""

        return False, f"{self.message} ({' ,'.join(offending_keys)})"
