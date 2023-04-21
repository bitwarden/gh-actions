from collections.abc import Callable

from .models.workflow import Workflow
from .models.job import Job
from .models.step import Step


class LintFinding:
    """Represents a linting problem."""
    description: str = "<no description>"
    level: str = None


def _validate(
    obj: Workflow | Job | Step,
    rule: Callable[[Workflow | Job | Step], bool | None],
    message: str,
    warning_level: str
) -> LintFinding | None:
    try:
        if rule(obj):
            return None
    except:
        message = f"failed to apply {rule.__name__}"
        warning_level = "error"

    return LintFinding(f"{obj.__name__}.{obj.name} => {message}", warning_level)


# -------- Rules ---------

def workflow_name_exists( obj: Workflow | Job | Step):
    return obj.name is not None

def workflow_name_capitalized( obj: Workflow | Job | Step):
    return obj.name.isupper()

# ----- End of Rules -----


findings = list(filter(lambda a: a is not None, [
    _validate(workflow, workflow_name_exists, "field required", "error"),
    _validate(workflow, workflow_name_capitalized, "field must be capitalized", "error")
]))
