"""Test src/models/workflow.py."""

import pytest

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.bitwarden_workflow_linter.models.job import Job
from src.bitwarden_workflow_linter.models.step import Step
from src.bitwarden_workflow_linter.models.workflow import Workflow


yaml = YAML()


@pytest.fixture(name="simple_workflow_yaml")
def fixture_simple_workflow_yaml():
    return yaml.load(
        """\
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
    )


@pytest.fixture(name="complex_workflow_yaml")
def fixture_complex_workflow_yaml():
    return yaml.load(
        """\
---
name: test
on:
  workflow_dispatch:
  pull_request:

jobs:
  job-key:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: echo test

  call-workflow:
    uses: bitwarden/server/.github/workflows/workflow-linter.yml@master

  test-normal-action:
    name: Download Latest
    runs-on: ubuntu-20.04
    steps:
      - name: Checkout
        uses: actions/checkout@2541b1294d2704b0964813337f33b291d3f8596b

      - run: |
          echo test

  test-local-action:
    name: Testing a local action call
    runs-on: ubuntu-20.04
    steps:
      - name: local-action
        uses: ./version-bump
"""
    )


def test_simple_workflow(simple_workflow_yaml):
    workflow = Workflow.init("", simple_workflow_yaml)

    assert workflow.name == "test"
    assert len(workflow.on.keys()) == 1
    assert len(workflow.jobs.keys()) == 1


def test_complex_workflow(complex_workflow_yaml):
    workflow = Workflow.init("", complex_workflow_yaml)

    assert workflow.name == "test"
    assert len(workflow.on.keys()) == 2
    assert len(workflow.jobs.keys()) == 4


def test_workflow_extra_kwargs(simple_workflow_yaml):
    extra_data_workflow = simple_workflow_yaml
    extra_data_workflow["extra"] = "This should not exist"

    workflow = Workflow.init("", extra_data_workflow)

    with pytest.raises(Exception):
        assert workflow.extra == "test"
