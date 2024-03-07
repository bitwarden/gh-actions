"""Test src/bitwarden_workflow_linter/rules/step_pinned.py."""

import pytest

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.rules.step_pinned import RuleStepUsesPinned

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
    steps:
      - name: Test 3rd Party Action
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Test Internal Action
        uses: bitwarden/gh-actions/get-keyvault-secrets@main

      - name: Test Local Action
        uses: ./actions/test-action

      - name: Test Run Action
        run: echo "test"
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
    steps:
      - name: Test External Branch
        uses: actions/checkout@main

      - name: Test Incorrect Hex
        uses: actions/checkout@b4ffde

      - name: Test Internal Commit
        uses: bitwarden/gh-actions/get-keyvault-secrets@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="rule")
def fixture_rule():
    return RuleStepUsesPinned()


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[0])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[1])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[2])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[3])
    assert result is True


def test_rule_on_incorrect_workflow_external_branch(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[0])
    assert result is False
    assert "Please pin the action" in message


def test_rule_on_incorrect_workflow_hex(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[1])
    assert result is False
    assert "Please use the full commit sha" in message


def test_rule_on_incorrect_workflow_internal_commit(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[2])
    assert result is False
    assert "Please pin to main" in message


def test_fail_compatibility(rule, correct_workflow):
    finding = rule.execute(correct_workflow)
    assert "Workflow not compatible with" in finding.description

    finding = rule.execute(correct_workflow.jobs["job-key"])
    assert "Job not compatible with" in finding.description
