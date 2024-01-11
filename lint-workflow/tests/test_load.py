"""Tests src/load.py."""
import pytest

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .conftest import FIXTURE_DIR

from src.load import WorkflowBuilder
from src.models.workflow import Workflow


yaml = YAML()


@pytest.fixture(name="workflow_filename")
def fixture_workflow_filename():
    return f"{FIXTURE_DIR}/test.yml"


@pytest.fixture(name="workflow_yaml")
def fixture_workflow_yaml():
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


def test_load_workflow_from_file(workflow_filename: str) -> None:
    workflow = WorkflowBuilder.build(workflow_filename)
    assert isinstance(workflow, Workflow)


def test_load_workflow_from_yaml(workflow_yaml: CommentedMap) -> None:
    workflow = WorkflowBuilder.build(workflow=workflow_yaml, from_file=False)
    assert isinstance(workflow, Workflow)
