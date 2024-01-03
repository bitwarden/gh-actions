import pytest

from ruamel.yaml import YAML

from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.name_capitalized import RuleNameCapitalized

yaml = YAML()


@pytest.fixture
def correct_workflow():
    return WorkflowBuilder.build(f"{FIXTURE_DIR}/test-min.yaml")


@pytest.fixture
def incorrect_workflow_name():
    workflow = """\
---
name: test
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
def incorrect_job_name():
    workflow = """\
---
name: Test
on:
  workflow_dispatch:

jobs:
  job-key:
    name: test
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: echo test
"""
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def incorrect_step_name():
    workflow = """\
---
name: Test
on:
  workflow_dispatch:

jobs:
  job-key:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: test
        run: echo test
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


def test_rule_on_incorrect_workflow_name(rule, incorrect_workflow_name):
    result, message = rule.fn(incorrect_workflow_name)
    assert result == False


def test_rule_on_incorrect_workflow_name(rule, incorrect_job_name):
    result, message = rule.fn(incorrect_job_name.jobs["job-key"])
    assert result == False


def test_rule_on_incorrect_workflow_name(rule, incorrect_step_name):
    result, message = rule.fn(incorrect_step_name.jobs["job-key"].steps[0])
    assert result == False
