"""Test src/bitwarden_workflow_linter/rules/job_environment_prefix."""

import pytest

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.rules.job_environment_prefix import (
    RuleJobEnvironmentPrefix,
)

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


@pytest.fixture(name="no_env_workflow")
def fixture_no_env_workflow():
    workflow = """\
---
on:
  workflow_dispatch:

jobs:
  job-key:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="missing_prefix_workflow")
def fixture_missing_prefix_workflow():
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


def test_rule_on_no_env_workflow(rule, no_env_workflow):
    obj = no_env_workflow.jobs["job-key"]

    result, message = rule.fn(no_env_workflow.jobs["job-key"])
    assert result is True
    assert message == ""

    finding = rule.execute(obj)
    assert finding is None


def test_rule_on_missing_prefix_workflow(rule, missing_prefix_workflow):
    obj = missing_prefix_workflow.jobs["job-key"]

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
