import json
import pytest

from .conftest import FIXTURE_DIR
from .context import src


@pytest.fixture
def workflow_default_data():
    return {
        "name": "Test Workflow",
        "on": {},
        "jobs": {
            "job-key": src.models.Job.from_dict({
                "name": "Test",
                "runs-on": "ubuntu-latest",
                "steps": [src.models.Step.from_dict({ "run": "echo stub"})]
            })
        }
    }


def test_workflow_default(workflow_default_data):
    workflow = src.models.Workflow(**workflow_default_data)

    assert workflow.name == "Test Workflow"
    assert len(workflow.on.keys()) == 0
    assert len(workflow.jobs.keys()) == 1


def test_workflow_extra_kwargs(workflow_default_data):
    workflow = src.models.Workflow.from_dict({
        "extra": "test",
        **workflow_default_data
    })

    with pytest.raises(Exception) as e_info:
        assert workflow.extra == "test"
