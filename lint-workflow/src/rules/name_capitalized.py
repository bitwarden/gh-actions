from typing import Union, Tuple

from ..rule import Rule
from ..models.workflow import Workflow
from ..models.job import Job
from ..models.step import Step
from ..utils import Settings


class RuleNameCapitalized(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = "name must capitalized"
        self.on_fail = "error"
        self.settings = settings

    def fn(self, obj: Union[Workflow, Job, Step]) -> Tuple[bool, str]:
        if obj.name:
            return obj.name[0].isupper(), self.message
        return True, ""  # Force passing if obj.name doesn't exist
