import json
import pytest

from ruamel.yaml.comments import CommentedMap

from .conftest import FIXTURE_DIR
from .context import src


@pytest.fixture
def workflow_filename():
    return f"{FIXTURE_DIR}/test.yml"


def test_load_workflow(workflow_filename):
    workflow = src.load.WorkflowBuilder.build(workflow_filename)
    assert type(workflow) == src.models.Workflow
