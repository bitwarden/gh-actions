from ..rule import Rule
from ..models.job import Job


class RuleJobEnvironmentPrefix(Rule):
    def __init__(self):
        self.message = f"Job Environment vars should start with and underscore:\n"
        self.on_fail = "error"
        self.compability = [Job]

    def fn(self, obj: Job):
        correct = True
        message = ""

        for key, value in obj.env.items():
            if key[0] != "_":
                message += f"  {key}"
                correct = False

        if correct:
            return True, ""

        return False, f"{self.message}{message}"
