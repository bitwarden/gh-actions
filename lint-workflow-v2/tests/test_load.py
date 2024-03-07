"""Tests src/bitwarden_workflow_linter/load.py."""

import pytest

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .conftest import FIXTURE_DIR

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.models.workflow import Workflow


yaml = YAML()


@pytest.fixture(name="workflow_filename")
def fixture_workflow_filename():
    return f"{FIXTURE_DIR}/test.yml"


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


def test_load_workflow_from_file(workflow_filename: str) -> None:
    workflow = WorkflowBuilder.build(workflow_filename)
    assert isinstance(workflow, Workflow)


def test_load_simple_workflow_from_yaml(simple_workflow_yaml: CommentedMap) -> None:
    workflow = WorkflowBuilder.build(workflow=simple_workflow_yaml, from_file=False)
    assert isinstance(workflow, Workflow)


def test_load_complex_workflow_from_yaml(complex_workflow_yaml: CommentedMap) -> None:
    workflow = WorkflowBuilder.build(workflow=complex_workflow_yaml, from_file=False)
    assert isinstance(workflow, Workflow)
