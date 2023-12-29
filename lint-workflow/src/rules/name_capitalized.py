from typing import Union

from ..rule import Rule
from ..models.workflow import Workflow
from ..models.job import Job
from ..models.step import Step


class RuleNameCapitalized(Rule):
    def __init__(self):
        self.message = "name must capitalized"
        self.on_fail = "error"

    def fn(self, obj: Union[Workflow, Job, Step]):
        if obj.name:
            return obj.name[0].isupper()
        return True  # Force passing if obj.name doesn't exist
