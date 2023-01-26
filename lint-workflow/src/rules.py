class LintFinding:
    """Represents a linting problem."""

    def __init__(self, description="<no description>", level=None):
        self.description = description
        self.level = level


class Rule:
    def __init__(self, obj, field, rule, failure_message, failure_level="warning"):
        self.obj = obj
        self.field = field
        self.rule = rule
        self.failure_level = failure_level
        self.failure_message = failure_message

    def run(self):
        failure_message = f"{self.obj}.{self.field} => {self.failure_message}"

        if not self.rule(self.obj[self.field]):
            return LintFinding(failure_message, self.failure_level)
        return None


def enforce_field_exists(field):
    return False if field is None else return True

def enforce_field_starts_upper(field):
    if field is None or not field[0].isupper():
        return False
    return True


findings = []

rules: [
    Rule(workflow, "name", enforce_field_exists, "field required", "error")
    Rule(workflow, "name", enforce_field_starts_upper, "field must be capitalized", "error")
]


for rule in rules:
    findings.append(rule.run())
