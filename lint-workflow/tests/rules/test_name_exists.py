import pytest
from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.name_exists import RuleNameExists


@pytest.fixture
def correct_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min.yaml")


@pytest.fixture
def incorrect_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min-incorrect.yaml")


@pytest.fixture
def rule():
    return RuleNameExists()


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, message = rule.fn(correct_workflow)
    assert result == True

    result, message = rule.fn(correct_workflow.jobs["job-key"])
    assert result == True

    result, message = rule.fn(correct_workflow.jobs["job-key"].steps[0])
    assert result == True


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    print(f"Workflow name: {incorrect_workflow.name}")
    result, message = rule.fn(incorrect_workflow)
    assert result == False

    result, message = rule.fn(incorrect_workflow.jobs["job-key"])
    assert result == False

    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[0])
    assert result == False
