from dataclasses import dataclass
from typing import Self


@dataclass
class Colors:
    """Class containing color codes for printing strings to output."""

    black = "30m"
    red = "31m"
    green = "32m"
    yellow = "33m"
    blue = "34m"
    magenta = "35m"
    cyan = "36m"
    white = "37m"


@dataclass
class LintFinding:
    """Represents a linting problem."""

    description: str = "<no description>"
    level: str = None


@dataclass
class Action:
    name: str
    version: str = ""
    sha: str = ""

    def __eq__(self, other: Self) -> bool:
        return (
            self.name == other.name
            and self.version == other.version
            and self.sha == other.sha
        )

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)


class SettingsError(Exception):
    pass


@dataclass
class Settings:
    enabled_rules: list[str]
    approved_actions: dict[str, Action]

    def __init__(
        self,
        enabled_rules: list[str] = None,
        approved_actions: dict[str, dict[str, str]] = None,
    ):
        self.enabled_rules = enabled_rules
        self.approved_actions = {
            name: Action(**action) for name, action in approved_actions.items()
        }
