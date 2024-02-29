"""Tests src/bitwarden_workflow_linter/rule.py."""

import pytest
from typing import Union

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.models.job import Job
from src.bitwarden_workflow_linter.models.step import Step
from src.bitwarden_workflow_linter.models.workflow import Workflow
from src.bitwarden_workflow_linter.rule import Rule, RuleExecutionException


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
        uses: actions/checkout@main
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
      - uses: actions/checkout@main
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


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
        return obj.name is not None, self.message


class RuleException(Rule):
    def __init__(self):
        self.message = "should raise Exception"
        self.on_fail = "error"

    def fn(self, obj: Union[Workflow, Job, Step]) -> bool:
        raise RuleExecutionException("test Exception")


@pytest.fixture(name="step_rule")
def fixture_step_rule():
    return RuleStep()


@pytest.fixture(name="exists_rule")
def fixture_exists_rule():
    return RuleNameExists()


@pytest.fixture(name="exception_rule")
def fixture_exception_rule():
    return RuleException()


def test_build_lint_message(step_rule, correct_workflow):
    assert step_rule.build_lint_message("test", correct_workflow) == "Workflow => test"

    assert (
        step_rule.build_lint_message("test", correct_workflow.jobs["job-key"])
        == "Job [job-key] => test"
    )

    assert (
        step_rule.build_lint_message("test", correct_workflow.jobs["job-key"].steps[0])
        == "Step [job-key.0] => test"
    )


def test_rule_compatibility(step_rule, correct_workflow):
    assert "not compatible" in step_rule.execute(correct_workflow).description
    assert (
        "not compatible"
        in step_rule.execute(correct_workflow.jobs["job-key"]).description
    )
    assert (
        "not compatible"
        not in step_rule.execute(correct_workflow.jobs["job-key"].steps[0]).description
    )


def test_correct_rule_execution(exists_rule, correct_workflow):
    assert exists_rule.execute(correct_workflow) is None
    assert exists_rule.execute(correct_workflow.jobs["job-key"]) is None
    assert exists_rule.execute(correct_workflow.jobs["job-key"].steps[0]) is None


def test_incorrect_rule_execution(exists_rule, incorrect_workflow):
    assert "name must exist" in exists_rule.execute(incorrect_workflow).description
    assert (
        "name must exist"
        in exists_rule.execute(incorrect_workflow.jobs["job-key"]).description
    )
    assert (
        "name must exist"
        in exists_rule.execute(incorrect_workflow.jobs["job-key"].steps[0]).description
    )


def test_exception_rule_execution(exception_rule, incorrect_workflow):
    assert "failed to apply" in exception_rule.execute(incorrect_workflow).description
