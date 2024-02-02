"""Test src/models/job.py."""

import pytest

from src.bitwarden_workflow_linter.models.job import Job
from src.bitwarden_workflow_linter.models.step import Step


@pytest.fixture(name="default_job_data")
def fixture_default_job_data():
    return {
        "name": "Test",
        "runs-on": "ubuntu-latest",
        "steps": [Step(run="echo stub")],
    }


@pytest.fixture(name="default_job")
def fixture_default_job(default_job_data):
    return Job.init("default-job", default_job_data)


def test_job_default(default_job):
    assert default_job.key == "default-job"
    assert default_job.name == "Test"
    assert default_job.runs_on == "ubuntu-latest"
    assert default_job.env is None
    assert len(default_job.steps) == 1


def test_job_extra_kwargs(default_job_data):
    job = Job.init("test-job", {"extra": "test", **default_job_data})

    with pytest.raises(Exception):
        assert job.extra == "test"
