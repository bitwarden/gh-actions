import json
import pytest

from .conftest import FIXTURE_DIR
from .context import src


@pytest.fixture
def workflow_filename():
    return f"{FIXTURE_DIR}/test.yml"


def test_load_workflow(workflow_filename):
    loaded_yaml = src.load.load_workflow(workflow_filename)
    print(loaded_yaml)
    print(type(loaded_yaml))
    print(dir(loaded_yaml))

    assert False


def test_build_workflow(workflow_filename):
    workflow = src.load.build_workflow(
        src.load.load_workflow(workflow_filename)
    )

    assert workflow.name == "crowdin Pull"
    assert len(workflow.jobs["crowdin-pull"].steps) == 4
