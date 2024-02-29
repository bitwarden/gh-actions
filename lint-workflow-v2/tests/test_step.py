"""Test src/bitwarden_workflow_linter/models/step.py."""

import json
import pytest

from ruamel.yaml import YAML

from src.bitwarden_workflow_linter.models.step import Step


@pytest.fixture(name="default_step")
def fixture_default_step():
    step_str = """\
name: Default Step
run: echo "test"
"""
    yaml = YAML()
    step_yaml = yaml.load(step_str)
    return Step.init(0, "default", step_yaml)


@pytest.fixture(name="uses_step")
def fixture_uses_step():
    step_str = """\
name: Download Artifacts
uses: bitwarden/download-artifacts@main # v1.0.0
with:
    workflow: upload-test-artifacts.yml
    artifacts: artifact
    path: artifact
    branch: main

"""
    yaml = YAML()
    step_yaml = yaml.load(step_str)
    return Step.init(0, "default", step_yaml)


def test_step_default(default_step):
    assert default_step.key == 0
    assert default_step.job == "default"
    assert default_step.name == "Default Step"
    assert default_step.env is None
    assert default_step.uses is None
    assert default_step.uses_with is None
    assert default_step.run == 'echo "test"'


def test_step_no_keyword_field(default_step):
    assert default_step.uses_with is None
    assert "uses_with" not in default_step.to_json()


def test_step_extra_kwargs(default_step):
    with pytest.raises(Exception):
        assert default_step.extra == "test"


def test_step_keyword_field(uses_step):
    expected_response = {
        "workflow": "upload-test-artifacts.yml",
        "artifacts": "artifact",
        "path": "artifact",
        "branch": "main",
    }

    step_json = uses_step.to_json()
    assert uses_step.key == 0
    assert "uses_with" not in step_json
    assert "with" in step_json
    assert json.loads(uses_step.to_json())["with"] == expected_response


def test_step_comment(uses_step):
    assert uses_step.key == 0
    assert uses_step.job == "default"
    assert uses_step.uses_comment is not None
    assert uses_step.uses_comment == "# v1.0.0"
