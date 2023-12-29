import pytest

from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.name_capitalized import RuleNameCapitalized


@pytest.fixture
def correct_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min.yaml")


@pytest.fixture
def incorrect_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min-incorrect.yaml")


@pytest.fixture
def rule():
    return RuleNameCapitalized()


def test_rule_on_correct_workflow(rule, correct_workflow):
    assert rule.fn(correct_workflow) == True
    assert rule.fn(correct_workflow.jobs['job-key']) == True
    assert rule.fn(correct_workflow.jobs['job-key'].steps[0]) == True


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    print(f"Workflow name: {incorrect_workflow.name}")
    assert rule.fn(incorrect_workflow) == False
    assert rule.fn(incorrect_workflow.jobs['job-key']) == False
    assert rule.fn(incorrect_workflow.jobs['job-key'].steps[0]) == False
