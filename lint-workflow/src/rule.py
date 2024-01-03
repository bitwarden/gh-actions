from typing import Union, List

from .models.workflow import Workflow
from .models.job import Job
from .models.step import Step
from .utils import LintFinding, Settings


class Rule:
    message: str = "error"
    on_fail: str = "error"
    compatibility: List[Union[Workflow, Job, Step]] = [Workflow, Job, Step]
    settings: Settings = None

    def fn(self, obj: Union[Workflow, Job, Step]) -> bool:
        return False, self.message

    def build_lint_message(self, message: str, obj: Union[Workflow, Job, Step]) -> str:
        obj_type = type(obj)

        if obj_type == Step:
            return f"{obj_type.__name__} [{obj.job}.{obj.key}] => {message}"
        elif obj_type == Job:
            return f"{obj_type.__name__} [{obj.key}] => {message}"
        else:
            return f"{obj_type.__name__} => {message}"

    def execute(self, obj: Union[Workflow, Job, Step]) -> Union[LintFinding, None]:
        message = None

        if type(obj) not in self.compatibility:
            return LintFinding(
                self.build_lint_message(
                    f"{type(obj).__name__} not compatible with {type(self).__name__}",
                    obj,
                ),
                "error",
            )

        try:
            passed, message = self.fn(obj)

            if passed:
                return None
        except Exception as err:
            return LintFinding(
                self.build_lint_message(
                    f"failed to apply {type(self).__name__}\n{err}", obj
                ),
                "error",
            )

        return LintFinding(self.build_lint_message(message, obj), self.on_fail)
