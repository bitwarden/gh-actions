import pytest

from ruamel.yaml import YAML

from ..conftest import FIXTURE_DIR
from ..context import src

from src.load import WorkflowBuilder
from src.rules.pinned_job_runner import RuleJobRunnerVersionPinned

yaml = YAML()


@pytest.fixture
def correct_runner():
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
    return WorkflowBuilder.build(yaml=yaml.load(workflow), from_file=False)


@pytest.fixture
def incorrect_runner():
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
    return RuleJobRunnerVersionPinned()


def test_rule_on_correct_runner(rule, correct_runner):
    result, message = rule.fn(correct_runner.jobs["job-key"])
    assert result == True


def test_rule_on_incorrect_runner(rule, incorrect_runner):
    result, message = rule.fn(incorrect_runner.jobs["job-key"])
    assert result == False
