"""Test src/models/workflow.py."""

import pytest

from src.models.job import Job
from src.models.step import Step
from src.models.workflow import Workflow


@pytest.fixture(name="default_workflow_data")
def fixture_default_workflow_data():
    return {
        "name": "Test Workflow",
        "on": {},
        "jobs": {
            "job-key": Job.from_dict(
                {
                    "name": "Test",
                    "runs-on": "ubuntu-latest",
                    "steps": [Step.from_dict({"run": "echo stub"})],
                }
            )
        },
    }


def test_workflow_default(default_workflow_data):
    workflow = Workflow(**default_workflow_data)

    assert workflow.name == "Test Workflow"
    assert len(workflow.on.keys()) == 0
    assert len(workflow.jobs.keys()) == 1


def test_workflow_extra_kwargs(default_workflow_data):
    workflow = Workflow.from_dict({"extra": "test", **default_workflow_data})

    with pytest.raises(Exception):
        assert workflow.extra == "test"
