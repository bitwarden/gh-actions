import json
import os


enabled_rules = [
    "src.rules.name_exists.RuleNameExists",
    "src.rules.name_capitalized.RuleNameCapitalized",
    "src.rules.pinned_job_runner.RuleJobRunnerVersionPinned",
    "src.rules.job_environment_prefix.RuleJobEnvironmentPrefix",
    "src.rules.step_pinned.RuleStepUsesPinned",
]


with open("actions.json", "r") as action_file:
    approved_actions = json.loads(action_file.read())
