"""Test src/bitwarden_workflow_linter/rules/step_approved.py."""

import pytest

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.rules.step_approved import RuleStepUsesApproved
from src.bitwarden_workflow_linter.utils import Settings


yaml = YAML()


@pytest.fixture(name="settings")
def fixture_settings():
    return Settings(
        approved_actions={
            "actions/checkout": {
                "name": "actions/checkout",
                "version": "v4.1.1",
                "sha": "b4ffde65f46336ab88eb53be808477a3936bae11",
            },
            "actions/download-artifact": {
                "name": "actions/download-artifact",
                "version": "v4.1.0",
                "sha": "f44cd7b40bfd40b6aa1cc1b9b5b7bf03d3c67110",
            },
        }
    )


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
      - name: Checkout Branch
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Test Bitwarden Action
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
      - name: Checkout Branch
        uses: joseph-flinn/action-DNE@main

      - name: Out of date action
        uses: actions/download-artifact@7a1cd3216ca9260cd8022db641d960b1db4d1be4 # v4.0.0
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="rule")
def fixture_rule(settings):
    return RuleStepUsesApproved(settings=settings)


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[0])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[1])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[2])
    assert result is True

    result, _ = rule.fn(correct_workflow.jobs["job-key"].steps[3])
    assert result is True


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[0])
    assert result is False
    assert "New Action detected" in message

    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[1])
    assert result is False
    assert "Action is out of date" in message


def test_fail_compatibility(rule, correct_workflow):
    finding = rule.execute(correct_workflow)
    assert "Workflow not compatible with" in finding.description

    finding = rule.execute(correct_workflow.jobs["job-key"])
    assert "Job not compatible with" in finding.description
