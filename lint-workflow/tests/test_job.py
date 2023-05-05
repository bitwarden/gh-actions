import json
import pytest

from .context import src


@pytest.fixture
def job_default_data():
    return {
        "name": "Test",
        "runs-on": "ubuntu-latest",
        "steps": [src.models.Step(run="echo stub")]
    }


def test_job_default(job_default_data):
    job = src.models.Job.from_dict(job_default_data)

    assert job.name == "Test"
    assert job.runs_on == "ubuntu-latest"
    assert job.env == None
    assert len(job.steps) == 1


def test_job_extra_kwargs(job_default_data):
    job = src.models.Job.from_dict({
        "extra": "test",
        **job_default_data
    })

    with pytest.raises(Exception) as e_info:
        assert job.extra == "test"
