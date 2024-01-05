import pytest

from ruamel.yaml import YAML

from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.step_approved import RuleStepUsesApproved
from src.utils import Settings


yaml = YAML()


@pytest.fixture
def settings():
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


@pytest.fixture
def correct_workflow():
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
"""
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def incorrect_workflow():
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
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def rule(settings):
    return RuleStepUsesApproved(settings=settings)


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, message = rule.fn(correct_workflow.jobs["job-key"].steps[0])
    assert result == True

    result, message = rule.fn(correct_workflow.jobs["job-key"].steps[1])
    assert result == True


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[0])
    assert result == False
    assert "New Action detected" in message

    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[1])
    assert result == False
    assert "Action is out of date" in message
