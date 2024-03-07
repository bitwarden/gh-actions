"""Test src/bitwarden_workflow_linter/rules/name_exists.py."""

import pytest

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.rules.name_exists import RuleNameExists


yaml = YAML()


@pytest.fixture(name="correct_workflow")
def fixture_correct_workflow():
    workflow = """\
---
name: Test Workflow

on:
  workflow_dispatch:

jobs:
  job-key:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: echo test
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
    runs-on: ubuntu-latest
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="rule")
def fixture_rule():
    return RuleNameExists()


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, _ = rule.fn(correct_workflow)
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[0])
    assert result is True


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    print(f"Workflow name: {incorrect_workflow.name}")
    result, _ = rule.fn(incorrect_workflow)
    assert result is False

    result, _ = rule.fn(incorrect_workflow.jobs["job-key"])
    assert result is False

    result, _ = rule.fn(incorrect_workflow.jobs["job-key"].steps[0])
    assert result is False
