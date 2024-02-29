"""Base Rule class to build rules by extending."""

from typing import List, Optional, Tuple, Union

from .models.workflow import Workflow
from .models.job import Job
from .models.step import Step
from .utils import LintFinding, LintLevels, Settings


class RuleExecutionException(Exception):
    """Exception for the Base Rule class."""

    pass


class Rule:
    """Base class of a Rule to extend to create a linting Rule."""

    on_fail: LintLevels = LintLevels.ERROR
    compatibility: List[Union[Workflow, Job, Step]] = [Workflow, Job, Step]
    settings: Optional[Settings] = None

    def fn(self, obj: Union[Workflow, Job, Step]) -> Tuple[bool, str]:
        """Execute the Rule (this should be overridden in the extending class.

        Args:
          obj:
            The object that the Rule is to be run against

        Returns:
          The success/failure of the result of the Rule ran on the input.
        """
        return False, f"{obj.name}: <default fail message>"

    def build_lint_message(self, message: str, obj: Union[Workflow, Job, Step]) -> str:
        """Build the lint failure message.

        Build the lint failure message depending on the type of object that the
        Rule is being run against.

        Args:
          message:
            The message body of the failure
          obj:
            The object the Rule is being run against

        Returns:
          The type specific failure message
        """
        obj_type = type(obj)

        if obj_type == Step:
            return f"{obj_type.__name__} [{obj.job}.{obj.key}] => {message}"
        elif obj_type == Job:
            return f"{obj_type.__name__} [{obj.key}] => {message}"
        else:
            return f"{obj_type.__name__} => {message}"

    def execute(self, obj: Union[Workflow, Job, Step]) -> Union[LintFinding, None]:
        """Wrapper function to execute the overridden self.fn().

        Run the Rule against the object and return the results. The result
        could be an Exception message where the Rule cannot be run against
        the object for whatever reason. If an exception doesn't occur, the
        result is linting success or failure.

        Args:
          obj:
            The object the Rule is being run against

        Returns:
          A LintFinding object that contains the message to print to the user
          and a LintLevel that contains the level of error to calculate the
          exit code with.
        """
        message = None

        if type(obj) not in self.compatibility:
            return LintFinding(
                self.build_lint_message(
                    f"{type(obj).__name__} not compatible with {type(self).__name__}",
                    obj,
                ),
                LintLevels.ERROR,
            )

        try:
            passed, message = self.fn(obj)

            if passed:
                return None
        except RuleExecutionException as err:
            return LintFinding(
                self.build_lint_message(
                    f"failed to apply {type(self).__name__}\n{err}", obj
                ),
                LintLevels.ERROR,
            )

        return LintFinding(self.build_lint_message(message, obj), self.on_fail)
