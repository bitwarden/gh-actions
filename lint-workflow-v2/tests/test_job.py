"""Test src/bitwarden_workflow_linter/models/job.py."""

import pytest

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.bitwarden_workflow_linter.models.job import Job
from src.bitwarden_workflow_linter.models.step import Step


yaml = YAML()


@pytest.fixture(name="workflow_yaml")
def fixture_workflow_yaml():
    return yaml.load(
        """\
---
name: test
on:
  workflow_dispatch:
  pull_request:

jobs:
  job-key:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: echo test

  call-workflow:
    uses: bitwarden/server/.github/workflows/workflow-linter.yml@master

  test-normal-action:
    name: Download Latest
    runs-on: ubuntu-20.04
    steps:
      - name: Checkout
        uses: actions/checkout@2541b1294d2704b0964813337f33b291d3f8596b

      - run: |
          echo test

  test-local-action:
    name: Testing a local action call
    runs-on: ubuntu-20.04
    steps:
      - name: local-action
        uses: ./version-bump
"""
    )


def test_job_default(workflow_yaml):
    default_job_data = workflow_yaml["jobs"]["job-key"]
    default_job = Job.init("default-job", default_job_data)

    assert default_job.key == "default-job"
    assert default_job.name == "Test"
    assert default_job.runs_on == "ubuntu-latest"
    assert default_job.env is None
    assert len(default_job.steps) == 1


def test_uses_job(workflow_yaml):
    call_job_data = workflow_yaml["jobs"]["call-workflow"]
    call_job = Job.init("call-job", call_job_data)

    assert call_job.key == "call-job"
    assert call_job.uses is not None


def test_job_extra_kwargs(workflow_yaml):
    extra_data_job = workflow_yaml["jobs"]["job-key"]
    extra_data_job["extra"] = "This should not exist"

    job = Job.init("job-key", extra_data_job)

    with pytest.raises(Exception):
        assert job.extra == "test"
