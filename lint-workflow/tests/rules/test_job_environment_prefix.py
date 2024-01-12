"""Test src/rules/job_environment_prefix."""
import pytest

from ruamel.yaml import YAML

from src.load import WorkflowBuilder
from src.rules.job_environment_prefix import RuleJobEnvironmentPrefix

yaml = YAML()


@pytest.fixture(name="correct_workflow")
def fixture_correct_workflow():
    workflow = """\
---
on:
  workflow_dispatch:

jobs:
  job-key:
    runs-on: ubuntu-22.04
    env:
        _TEST_ENV: "test"
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="incorrect_workflow")
def fixture_incorrect_workflow():
    workflow = """\
---
on:
  workflow_dispatch:

jobs:
  job-key:
    runs-on: ubuntu-22.04
    env:
        TEST_ENV: "test"
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="rule")
def fixture_rule():
    return RuleJobEnvironmentPrefix()


def test_rule_on_correct_workflow(rule, correct_workflow):
    obj = correct_workflow.jobs["job-key"]

    result, message = rule.fn(correct_workflow.jobs["job-key"])
    assert result is True
    assert message == ""

    finding = rule.execute(obj)
    assert finding is None


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    obj = incorrect_workflow.jobs["job-key"]

    result, message = rule.fn(obj)
    assert result is False
    assert "TEST_ENV" in message

    finding = rule.execute(obj)
    assert "TEST_ENV" in finding.description


def test_fail_compatibility(rule, correct_workflow):
    finding = rule.execute(correct_workflow)
    assert "Workflow not compatible with" in finding.description

    finding = rule.execute(correct_workflow.jobs["job-key"].steps[0])
    assert "Step not compatible with" in finding.description
