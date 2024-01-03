from ..rule import Rule
from ..models.job import Job


class RuleJobRunnerVersionPinned(Rule):
    def __init__(self):
        self.message = "Workflow runner must be pinned"
        self.on_fail = "error"
        self.compatibility = [Job]

    def fn(self, obj: Job):
        if "latest" not in obj.runs_on:
            return True, ""
        return False, self.message
