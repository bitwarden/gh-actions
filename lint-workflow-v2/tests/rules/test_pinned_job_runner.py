"""Test src/bitwarden_workflow_linter/rules/pinned_job_runner.py."""

import pytest

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.rules.pinned_job_runner import (
    RuleJobRunnerVersionPinned,
)

yaml = YAML()


@pytest.fixture(name="correct_runner")
def fixture_correct_runner():
    workflow = """\
---
on:
  workflow_dispatch:

jobs:
  job-key:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test

  call-workflow:
    uses: bitwarden/server/.github/workflows/workflow-linter.yml@master
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="incorrect_runner")
def fixture_incorrect_runner():
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
    return RuleJobRunnerVersionPinned()


def test_rule_on_correct_runner(rule, correct_runner):
    result, _ = rule.fn(correct_runner.jobs["job-key"])
    assert result is True

    result, _ = rule.fn(correct_runner.jobs["call-workflow"])
    assert result is True


def test_rule_on_incorrect_runner(rule, incorrect_runner):
    result, _ = rule.fn(incorrect_runner.jobs["job-key"])
    assert result is False
