import json
import pytest

from .context import src


@pytest.fixture
def workflow_default_data():
    return {
        "name": "Test Workflow",
        "on": {},
        "jobs": {
            "job-key": src.models.Job(**{
                "name": "Test",
                "runs-on": "ubuntu-latest",
                "steps": [src.models.Step(run="echo stub")]
            })
        }
    }


def test_workflow_creation(workflow_default_data):
    workflow = src.models.Workflow(**workflow_default_data)

    assert workflow.name == "Test Workflow"
