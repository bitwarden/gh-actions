from typing import Union, Tuple

from ..rule import Rule
from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..utils import LintLevels, Settings


class RuleJobRunnerVersionPinned(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = "Workflow runner must be pinned"
        self.on_fail: LintLevels = LintLevels.ERROR
        self.compatibility: List[Union[Workflow, Job, Step]] = [Job]
        self.settings: Settings = settings

    def fn(self, obj: Job) -> Tuple[bool, str]:
        """Enforces runners are pinned to a version

        Example:
        ---
        on:
          workflow_dispatch:

        jobs:
          job-key:
            runs-on: ubuntu-22.04
            steps:
              - run: echo test

        'runs-on' is pinned to '22.04' instead of 'latest'
        """
        if "latest" not in obj.runs_on:
            return True, ""
        return False, self.message
