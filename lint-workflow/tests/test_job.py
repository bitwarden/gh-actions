import json
import pytest

from .context import src


@pytest.fixture
def default_job_data():
    return {
        "name": "Test",
        "runs-on": "ubuntu-latest",
        "steps": [src.models.Step(run="echo stub")],
    }


@pytest.fixture
def default_job(default_job_data):
    return src.models.Job.init("default-job", default_job_data)


def test_job_default(default_job):
    assert default_job.key == "default-job"
    assert default_job.name == "Test"
    assert default_job.runs_on == "ubuntu-latest"
    assert default_job.env == None
    assert len(default_job.steps) == 1


def test_job_extra_kwargs(default_job_data):
    job = src.models.Job.init("test-job", {"extra": "test", **default_job_data})

    with pytest.raises(Exception) as e_info:
        assert job.extra == "test"
