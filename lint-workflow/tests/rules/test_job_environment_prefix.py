import pytest

from ruamel.yaml import YAML

from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.job_environment_prefix import RuleJobEnvironmentPrefix

yaml = YAML()


@pytest.fixture
def correct_workflow():
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
    env:
        TEST_ENV: "test"
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def rule():
    return RuleJobEnvironmentPrefix()


def test_rule_on_correct_workflow(rule, correct_workflow):
    result, message = rule.fn(correct_workflow.jobs["job-key"])
    assert result == True
    assert message == ""


def test_rule_on_incorrect_workflow(rule, incorrect_workflow):
    result, message = rule.fn(incorrect_workflow.jobs["job-key"])
    assert result == False
    assert "TEST_ENV" in message
