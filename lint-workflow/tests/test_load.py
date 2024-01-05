import json
import pytest

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .conftest import FIXTURE_DIR
from .context import src

from src.utils import Settings


yaml = YAML()


@pytest.fixture
def workflow_filename():
    return f"{FIXTURE_DIR}/test.yml"


@pytest.fixture
def workflow_yaml():
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
    workflow = src.load.WorkflowBuilder.build(workflow_filename)
    assert type(workflow) == src.models.Workflow


def test_load_workflow_from_yaml(workflow_yaml: CommentedMap) -> None:
    workflow = src.load.WorkflowBuilder.build(yaml=workflow_yaml, from_file=False)
    assert type(workflow) == src.models.Workflow
