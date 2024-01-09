from dataclasses import asdict, dataclass
from enum import Enum
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
class LintLevel:
    """Class to contain the numeric level and color of linting."""

    code: int
    color: Colors


class LintLevels(LintLevel, Enum):
    """Collection of the different types of LintLevels available."""

    NONE = 0, Colors.white
    WARNING = 1, Colors.yellow
    ERROR = 2, Colors.red


class LintFinding:
    """Represents a problem detected by linting."""

    def __init__(
        self, description: str = "<no description>", level: LintLevel = None
    ) -> None:
        self.description = description
        self.level = level

    def __str__(self) -> str:
        """String representation of the class.

        Returns:
        String representation of itself.
        """
        return f"\033[{self.level.color}{self.level.name.lower()}\033[0m {self.description}"


@dataclass
class Action:
    """Collection of the metadata associated with a GitHub Action."""

    name: str
    version: str = ""
    sha: str = ""

    def __eq__(self, other: Self) -> bool:
        """Override Action equality.

        Args:
          other:
            Another Action type object to compare

        Return
          The state of eqaulity
        """
        return (
            self.name == other.name
            and self.version == other.version
            and self.sha == other.sha
        )

    def __ne__(self, other: Self) -> bool:
        """Override Action unequality.

        Args:
          other:
            Another Action type object to compare

        Return
          The negation of the state of eqaulity
        """
        return not self.__eq__(other)


class SettingsError(Exception):
    """Custom Exception to indicate an error with loading Settings."""

    pass


class Settings:
    enabled_rules: list[str]
    approved_actions: dict[str, Action]

    def __init__(
        self,
        enabled_rules: list[str] = [],
        approved_actions: dict[str, dict[str, str]] = {},
    ):
        """Settings object that can be overriden in settings.py.

        Args:
          enabled_rules:
            All of the python modules that implement a Rule to be run against
            the workflows. These must be available somewhere on the PYTHONPATH
          approved_actions:
            The colleciton of GitHub Actions that are pre-approved to be used
            in any workflow (Required by src.rules.step_approved)
        """
        self.enabled_rules = enabled_rules
        self.approved_actions = {
            name: Action(**action) for name, action in approved_actions.items()
        }
