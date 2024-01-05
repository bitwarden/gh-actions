from typing import Tuple

from ..rule import Rule
from ..models.step import Step
from ..utils import Settings


class RuleStepUsesPinned(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = f"error"
        self.on_fail = "error"
        self.compatibility = [Step]
        self.settings = settings

    def force_pass(self, obj: Step) -> bool:
        if not obj.uses:
            return True, ""

        ## Force pass for any local actions
        if "@" not in obj.uses:
            return True

        return False

    def fn(self, obj: Step) -> Tuple[bool, str]:
        if self.force_pass(obj):
            return True, ""

        path, ref = obj.uses.split("@")

        if path.startswith("bitwarden/gh-actions"):
            if ref == "main":
                return True, ""
            return False, "Please pin to main"

        try:
            int(ref, 16)
        except:
            return False, "Please pin the action to a commit sha"

        if len(ref) != 40:
            return False, f"Please use the full commit sha to pin the action"

        return True, ""
