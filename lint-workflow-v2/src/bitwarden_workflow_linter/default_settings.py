"""This psuedo-module is essentially configuration-as-code."""

import json


enabled_rules = [
    "bitwarden_workflow_linter.rules.name_exists.RuleNameExists",
    "bitwarden_workflow_linter.rules.name_capitalized.RuleNameCapitalized",
    "bitwarden_workflow_linter.rules.pinned_job_runner.RuleJobRunnerVersionPinned",
    "bitwarden_workflow_linter.rules.job_environment_prefix.RuleJobEnvironmentPrefix",
    "bitwarden_workflow_linter.rules.step_pinned.RuleStepUsesPinned",
]


# with open("actions.json", "r", encoding="utf8") as action_file:
#    approved_actions = json.load(action_file)

# approved_actions = []

approved_actions_path = "default_actions.json"
