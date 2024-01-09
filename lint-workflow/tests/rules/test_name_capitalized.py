import pytest

from ruamel.yaml import YAML

from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.name_capitalized import RuleNameCapitalized

yaml = YAML()


@pytest.fixture
def correct_workflow():
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
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def incorrect_workflow():
    workflow = """\
---
name: test
on:
  workflow_dispatch:

jobs:
  job-key:
    name: test
    runs-on: ubuntu-latest
    steps:
      - name: test
        run: echo test
"""
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def missing_name_workflow():
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
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def rule():
    return RuleNameCapitalized()


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, message = rule.fn(correct_workflow)
    assert result == True

    result, message = rule.fn(correct_workflow.jobs["job-key"])
    assert result == True

    result, message = rule.fn(correct_workflow.jobs["job-key"].steps[0])
    assert result == True


def test_rule_on_incorrect_workflow_name(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow)
    assert result == False


def test_rule_on_incorrect_job_name(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"])
    assert result == False


def test_rule_on_incorrect_step_name(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"].steps[0])
    assert result == False


def test_rule_on_missing_names(rule, missing_name_workflow):
    result, message = rule.fn(missing_name_workflow)
    assert result == True

    result, message = rule.fn(missing_name_workflow.jobs["job-key"])
    assert result == True

    result, message = rule.fn(missing_name_workflow.jobs["job-key"].steps[0])
    assert result == True
