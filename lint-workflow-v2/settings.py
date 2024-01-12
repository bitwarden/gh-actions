"""This psuedo-module is essentially configuration-as-code."""
import json


enabled_rules = [
    "src.rules.name_exists.RuleNameExists",
    "src.rules.name_capitalized.RuleNameCapitalized",
    "src.rules.pinned_job_runner.RuleJobRunnerVersionPinned",
    "src.rules.job_environment_prefix.RuleJobEnvironmentPrefix",
    "src.rules.step_pinned.RuleStepUsesPinned",
]


with open("actions.json", "r", encoding="utf8") as action_file:
    approved_actions = json.load(action_file)
