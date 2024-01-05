from typing import Tuple

from ..rule import Rule
from ..models.job import Job
from ..utils import Settings


class RuleJobEnvironmentPrefix(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = f"Job Environment vars should start with and underscore:"
        self.on_fail = "error"
        self.compatibility = [Job]
        self.settings = settings

    def fn(self, obj: Job) -> Tuple[bool, str]:
        correct = True

        offending_keys = []
        for key, value in obj.env.items():
            if key[0] != "_":
                offending_keys.append(key)
                correct = False

        if correct:
            return True, ""

        return False, f"{self.message} ({' ,'.join(offending_keys)})"
