from dataclasses import dataclass


@dataclass
class LintFinding:
    """Represents a linting problem."""

    description: str = "<no description>"
    level: str = None


@dataclass
class Settings:
    enabled_rules: list[str]
    approved_actions_keys: set[str]
    approved_actions_data: dict[str, str]

    def __init__(
        self,
        enabled_rules: list[str] = None,
        approved_actions: list[dict[str, str]]= None
    ):
        self.enabled_rules = enabled_rules
        self.approved_actions = set([action['name'] for action in approved_actions])
        self.approved_actions_data = {
            action['name']: action for action in approved_actions
        }


class SettingsError(Exception):
    pass
