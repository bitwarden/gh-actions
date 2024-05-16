"""Test src/bitwarden_workflow_linter/rules/job_newlines."""

import pytest

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.rules.file_job_newlines import (
    RuleFileJobNewline,
)


@pytest.fixture(name="single_job_workflow")
def fixture_single_job_workflow():
    contents = """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=contents, from_file=False)


@pytest.fixture(name="correct_multi_job_workflow")
def fixture_correct_multi_job_workflow():
    contents = """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test

  second-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=contents, from_file=False)


@pytest.fixture(name="incorrect_multi_job_workflow")
def fixture_incorrect_multi_job_workflow():
    contents = """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test
  second-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test
"""
    return WorkflowBuilder.build(workflow=contents, from_file=False)


@pytest.fixture(name="rule")
def fixture_rule():
    return RuleFileJobNewline()


def test_rule_on_single_workflow(rule, single_job_workflow):
    workflow, file = single_job_workflow

    result, message = rule.fn(file)
    assert result is True
    assert message == ""

    finding = rule.execute(file)
    assert finding is None

    assert False

