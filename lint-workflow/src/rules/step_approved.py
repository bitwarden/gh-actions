from typing import Tuple

from ..rule import Rule
from ..models.step import Step
from ..utils import Settings


class RuleStepUsesApproved(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = f"error"
        self.on_fail = "warn"
        self.compatibility = [Step]
        self.settings = settings

    def force_pass(self, obj: Step) -> bool:
        ## Force pass for any shell steps
        if not obj.uses:
            return True, ""

        ## Force pass for any local actions
        if "@" not in obj.uses:
            return True

        ## Force pass for any bitwarden/gh-actions
        if obj.uses.startswith("bitwarden/gh-actions"):
            return True

        return False

    def fn(self, obj: Step) -> Tuple[bool, str]:
        if self.force_pass(obj):
            return True, ""

        path, hash = obj.uses.split("@")

        # Actions in bitwarden/gh-actions are auto-approved
        if not path in self.settings.approved_actions:
            return (
                False,
                (
                    f"New Action detected: {path}\n"
                    "For security purposes, actions must be reviewed and on the pre-approved list"
                ),
            )

        action = self.settings.approved_actions[path]

        if obj.uses_version != action.version or obj.uses_ref != action.sha:
            return False, (
                "Action is out of date. Please update to:\n"
                f"  commit: {action.version}"
                f"  version: {action.sha}"
            )

        return True, ""
