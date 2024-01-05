from typing import Tuple

from ..rule import Rule
from ..models.job import Job
from ..utils import Settings


class RuleJobRunnerVersionPinned(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = "Workflow runner must be pinned"
        self.on_fail = "error"
        self.compatibility = [Job]
        self.settings = settings

    def fn(self, obj: Job) -> Tuple[bool, str]:
        if "latest" not in obj.runs_on:
            return True, ""
        return False, self.message
