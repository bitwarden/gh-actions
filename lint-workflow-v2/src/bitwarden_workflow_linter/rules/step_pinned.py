"""A Rule to enforce Actions are pinned correctly."""

from typing import List, Optional, Tuple, Union

from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..rule import Rule
from ..utils import LintLevels, Settings


class RuleStepUsesPinned(Rule):
    """Rule to contain the enforcement logic for pinning Actions versions.

    Definition of Internal Action:
      An Action that exists in the `bitwarden/gh-actions` GitHub Repository.

    For any external Action (any Action that does not fit the above definition of
    an Internal Action), to mitigate the risks of supply chain attacks in our CI
    pipelines, we pin any use of an Action to a specific hash that has been verified
    and pre-approved after a security audit of the version of the Action.

    All Internl Actions, should be pinned to 'main'. This prevents Renovate from
    spamming a bunch of PRs across all of our repos when `bitwarden/gh-actions` is
    updated.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Constructor for RuleStepUsesPinned to override base Rule.

        Args:
          settings:
            A Settings object that contains any default, overriden, or custom settings
            required anywhere in the application.
        """
        self.on_fail = LintLevels.ERROR
        self.compatibility = [Step]
        self.settings = settings

    def skip(self, obj: Step) -> bool:
        """Skip this Rule on some Steps.

        This Rule does not apply to a few types of Steps. These
        Rules are skipped.
        """
        if not obj.uses:
            return True

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
        except ValueError:
            return False, "Please pin the action to a commit sha"

        if len(ref) != 40:
            return False, "Please use the full commit sha to pin the action"

        return True, ""
