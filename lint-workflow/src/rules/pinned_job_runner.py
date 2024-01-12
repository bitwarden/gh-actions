"""A Rule to enforce pinning runners to a specific OS version."""
from typing import List, Tuple, Union

from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..rule import Rule
from ..utils import LintLevels, Settings


class RuleJobRunnerVersionPinned(Rule):
    """Rule to enforce pinned Runner OS versions.

    `*-latest` versions updating without knowing has broken all of our worklfows
    in the past. To avoid this and prevent a single event from breaking the majority of
    our pipelines, we pin the versions.
    """
    def __init__(self, settings: Settings = None) -> None:
        """Constructor for RuleJobRunnerVersionPinned to override Rule class.

        Args:
          settings:
            A Settings object that contains any default, overriden, or custom settings
            required anywhere in the application.
        """
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
