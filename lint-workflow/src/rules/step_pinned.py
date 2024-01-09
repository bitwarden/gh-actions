from typing import Union, Tuple

from ..rule import Rule
from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..utils import LintLevels, Settings


class RuleStepUsesPinned(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = f"error"
        self.on_fail: LintLevels = LintLevels.ERROR
        self.compatibility: List[Union[Workflow, Job, Step]] = [Step]
        self.settings: Settings = settings

    def skip(self, obj: Step) -> bool:
        """Skip this Rule on some Steps.

        This Rule does not apply to a few types of Steps. These
        Rules are skipped.
        """
        if not obj.uses:
            return True, ""

        ## Force pass for any local actions
        if "@" not in obj.uses:
            return True

        return False

    def fn(self, obj: Step) -> Tuple[bool, str]:
        """Enforces all Actions to be pinned in a specific way.

        Pinning external Action hashes prevents unknown updates that could
        break the pipelines or be the entry point to a supply chain attack.

        Pinning internal Actions to branches allow for less updates as work
        is done on those repos. This is mainly to support our Action
        monorepo architecture of our Actions.

        Example:
        - name: Checkout Branch
          uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

        - name: Test Bitwarden Action
          uses: bitwarden/gh-actions/get-keyvault-secrets@main

        - name: Test Local Action
          uses: ./actions/test-action

        - name: Test Run Action
          run: echo "test"

        In this example, 'actions/checkout' must be pinned to the full commit
        of the tag while 'bitwarden/gh-actions/get-keyvault-secrets' must be
        pinned to 'main'. The other two Steps will be skipped.
        """
        if self.skip(obj):
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
