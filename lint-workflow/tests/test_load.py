import json
import pytest

from .conftest import FIXTURE_DIR
from .context import src


@pytest.fixture
def workflow_filename():
    return f"{FIXTURE_DIR}/test.yml"


def test_load_workflow(workflow_filename):
    workflow = src.load.load_workflow(workflow_filename)

    assert workflow.name == "crowdin Pull"
    assert len(workflow.jobs["crowdin-pull"].steps) == 4
    assert workflow.dict()["name"] == "crowdin Pull"

    print(workflow.dict(exclude_unset=True))

    assert False
