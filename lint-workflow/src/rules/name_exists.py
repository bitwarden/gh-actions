from typing import Union

from ..rule import Rule
from ..models.workflow import Workflow
from ..models.job import Job
from ..models.step import Step


class RuleNameExists(Rule):
    def __init__(self):
        self.message = "name must exist"
        self.on_fail = "error"

    def fn(self, obj: Union[Workflow, Job, Step]):
        return obj.name is not None
