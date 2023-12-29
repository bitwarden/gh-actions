import pytest
from typing import Union

from ruamel.yaml import YAML

from .conftest import FIXTURE_DIR
from .context import src

from src.load import WorkflowBuilder
from src.rule import Rule
from src.models import Workflow, Job, Step


class RuleStep(Rule):
    def __init__(self):
        self.message = "test"
        self.on_fail = "error"
        self.compatibility = [Step]


class RuleNameExists(Rule):
    def __init__(self):
        self.message = "name must exist"
        self.on_fail = "error"

    def fn(self, obj: Union[Workflow, Job, Step]) -> bool:
        print(f"{type(self).__name__}\n{obj}")
        return obj.name is not None


@pytest.fixture
def step_rule():
    return RuleStep()


@pytest.fixture
def exists_rule():
    return RuleNameExists()


@pytest.fixture
def correct_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min.yaml")


@pytest.fixture
def incorrect_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min-incorrect.yaml")


def test_build_lint_message(step_rule, correct_workflow):
    assert step_rule.build_lint_message(
        "test", correct_workflow
    ) == "Workflow => test"

    assert step_rule.build_lint_message(
        "test", correct_workflow.jobs['job-key']
    ) == "Job [job-key] => test"

    assert step_rule.build_lint_message(
        "test", correct_workflow.jobs['job-key'].steps[0]
    ) == "Step [job-key.0] => test"


def test_rule_compatibility(step_rule, correct_workflow):
    assert "not compatible" in step_rule.execute(correct_workflow).description
    assert "not compatible" in step_rule.execute(correct_workflow.jobs['job-key']).description
    assert "not compatible" not in step_rule.execute(
        correct_workflow.jobs['job-key'].steps[0]
    ).description


def test_correct_rule_execution(exists_rule, correct_workflow):
    assert exists_rule.execute(correct_workflow) == None
    assert exists_rule.execute(correct_workflow.jobs['job-key']) == None
    assert exists_rule.execute(correct_workflow.jobs['job-key'].steps[0]) == None


def test_incorrect_rule_execution(exists_rule, incorrect_workflow):
    assert "name must exist" in exists_rule.execute(incorrect_workflow).description
    assert "name must exist" in exists_rule.execute(incorrect_workflow.jobs['job-key']).description
    assert "name must exist" in exists_rule.execute(incorrect_workflow.jobs['job-key'].steps[0]).description