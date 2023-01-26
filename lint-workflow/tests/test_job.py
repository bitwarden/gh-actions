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


def test_job_creation(job_default_data):
    job = src.models.Job(**job_default_data)

    assert job.name == "Test"
