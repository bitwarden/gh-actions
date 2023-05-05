from collections.abc import Callable
from dataclasses import dataclass
from typing import Union

from .models.workflow import Workflow
from .models.job import Job
from .models.step import Step


@dataclass
class LintFinding:
    """Represents a linting problem."""
    description: str = "<no description>"
    level: str = None


def validate(
    obj: Union[Workflow, Job, Step],
    rule: Callable[Union[Workflow, Job, Step], Union[bool, None]],
    message: str,
    warning_level: str
) -> Union[LintFinding, None]:
    try:
        if rule(obj):
            return None
    except:
        message = f"failed to apply {rule.__name__}"
        warning_level = "error"

    return LintFinding(f"{obj.__name__}.{obj.name} => {message}", warning_level)


class Rule:
    def __init__(
        self,
        fn: Callable[Union[Workflow, Job, Step], Union[bool, None]],
        message: str = "error",
        warning_level: str = "error",
    ):
        self.fn = fn
        self.message = message
        self.warning_level = warning_level

    def execute(self, obj: Union[Workflow, Job, Step]):
        try:
            if self.fn(obj):
                return None
        except:
            message = f"failed to apply {self.fn.__name__}"
            warning_level = "error"

        #return LintFinding(f"{obj.__name__}.{obj.name} => {self.message}", self.warning_level)
        return LintFinding(f"{obj.name} => {self.message}", self.warning_level)


# -------- Rules ---------

def name_exists(obj: Union[Workflow, Job, Step]):
    return obj.name is not None

def name_capitalized(obj: Union[Workflow, Job, Step]):
    return obj.name.isupper()


def step_run_single_line(step: Step):
    return True

# ----- End of Rules -----

workflow_rules = [
    Rule(name_exists, "field required", "error"),
    Rule(name_capitalized, "field must be capitalized", "error")
]
job_rules = [
    Rule(name_exists, "field required", "error"),
    Rule(name_capitalized, "field must be capitalized", "error")
]
step_rules = [
    Rule(name_exists, "field required", "error"),
    Rule(name_capitalized, "field must be capitalized", "error")
]
uses_step_rules = [
]
run_step_rules = [
]

