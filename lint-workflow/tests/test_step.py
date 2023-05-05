import json
import pytest

from .context import src


@pytest.fixture
def step_default_data():
    return {
        "run": "echo \"test\""
    }


def test_step_default(step_default_data):
    step = src.models.Step.from_dict(step_default_data)
    assert step.name == None
    assert step.env == None
    assert step.uses == None
    assert step.run == "echo \"test\""


@pytest.mark.skip()
def test_step_keyword_field(step_default_data):
    data = {
        "with": {"config": "test.json"},
        **step_default_data
    }
    step = src.models.Step.from_dict(data)
    assert "with_field" not in step.json(by_alias=True)
    assert json.loads(step.json(by_alias=True))["with"] == {"config": "test.json"}


@pytest.mark.skip()
def test_step_no_keyword_field(step_default_data):
    step = src.models.Step.from_dict(step_default_data)
    assert step.with_field == None
    assert "with_field" not in step.json(by_alias=True)


def test_step_extra_kwargs(step_default_data):
    step = src.models.Step.from_dict({
        "name": "test step",
        "extra": "test",
        **step_default_data
    })

    with pytest.raises(Exception) as e_info:
        assert step.extra == "test"
