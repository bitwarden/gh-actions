from dataclasses import dataclass


@dataclass
class LintFinding:
    """Represents a linting problem."""
    description: str = "<no description>"
    level: str = None
