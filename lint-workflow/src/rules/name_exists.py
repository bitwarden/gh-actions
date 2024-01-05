from typing import Union, Tuple

from ..rule import Rule
from ..models.workflow import Workflow
from ..models.job import Job
from ..models.step import Step
from ..utils import Settings


class RuleNameExists(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = "name must exist"
        self.on_fail = "error"
        self.settings = settings

    def fn(self, obj: Union[Workflow, Job, Step]) -> Tuple[bool, str]:
        if obj.name is not None:
            return True, ""
        return False, self.message
