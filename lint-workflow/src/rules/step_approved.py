from typing import Union, Tuple

from ..rule import Rule
from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..utils import LintLevels, Settings


class RuleStepUsesApproved(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = f"error"
        self.on_fail: LintLevels = LintLevels.WARNING
        self.compatibility: List[Union[Workflow, Job, Step]] = [Step]
        self.settings: Settings = settings

    def skip(self, obj: Step) -> bool:
        """Skip this Rule on some Steps.

        This Rule does not apply to a few types of Steps. These
        Rules are skipped.
        """
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
        """Enforces all externally used Actions are on the pre-approved list.

        The pre-approved list allows tight auditing on what Actions are trusted
        and allowed to be run in our environments. This helps mitigate risks
        against supply chain attacks in our pipelines.

        Example:
        ---
        on:
          workflow_dispatch:

        jobs:
          job-key:
            runs-on: ubuntu-22.04
            steps:
              - name: Checkout Branch
                uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

              - name: Test Bitwarden Action
                uses: bitwarden/gh-actions/get-keyvault-secrets@main

              - name: Test Local Action
                uses: ./actions/test-action

              - name: Test Run Action
                run: echo "test"

        In this example, 'actions/checkout' must be on the pre-approved list
        and the metadata must match in order to succeed. The other three 
        Steps will be skipped.
        """
        if self.skip(obj):
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
