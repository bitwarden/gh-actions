"""Test src/bitwarden_workflow_linter/rules/job_newlines."""

import pytest

from src.bitwarden_workflow_linter.load import WorkflowBuilder
from src.bitwarden_workflow_linter.models.file_format import FileFormat
from src.bitwarden_workflow_linter.rules.file_job_newlines import (
    RuleFileJobNewline,
)


@pytest.fixture(name="correct_workflow_single_job")
def fixture_correct_workflow_single_job():
    return """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1
"""


@pytest.fixture(name="correct_workflow_multi_job")
def fixture_correct_workflow_multi_job():
    return """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1

  second-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test2
"""


@pytest.fixture(name="incorrect_workflow_single_job")
def fixture_incorrect_workflow_single_job():
    return """\
---
on:
  workflow_dispatch:

jobs:

  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1
"""


@pytest.fixture(name="incorrect_workflow_multi_job")
def fixture_incorrect_workflow_multi_job():
    return """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1
  second-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test2
"""


@pytest.fixture(name="correct_workflow_name_end")
def fixture_correct_workflow_name_end():
    return """\
---
on:
  workflow_dispatch:

jobs:
  job-name:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1

name: Test Workflow
"""


@pytest.fixture(name="correct_workflow_eof")
def fixture_correct_workflow_eof():
    return """\
---
on:
  workflow_dispatch:

jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1

  second-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test2"""


@pytest.fixture(name="incorrect_workflow_name_end")
def fixture_incorrect_workflow_name_end():
    return """\
---
on:
  workflow_dispatch:

jobs:
  job-name:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1
name: Test Workflow
"""


@pytest.fixture(name="rule")
def fixture_rule():
    return RuleFileJobNewline()


def test_get_job_block_single(rule, correct_workflow_single_job):
    expected = [
        "  first-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test1",
        "",
    ]

    workflow_lines = correct_workflow_single_job.split("\n")
    assert rule.get_job_blocks(workflow_lines) == expected


def test_get_job_block_multi(
    rule, correct_workflow_multi_job, incorrect_workflow_multi_job, correct_workflow_eof
):
    expected_correct = [
        "  first-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test1",
        "",
        "  second-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test2",
        "",
    ]

    expected_incorrect = [
        "  first-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test1",
        "  second-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test2",
        "",
    ]

    expected_eof = [
        "  first-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test1",
        "",
        "  second-job:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test2",
    ]

    workflow_lines = correct_workflow_multi_job.split("\n")
    assert rule.get_job_blocks(workflow_lines) == expected_correct

    workflow_lines = incorrect_workflow_multi_job.split("\n")
    assert rule.get_job_blocks(workflow_lines) == expected_incorrect

    workflow_lines = correct_workflow_eof.split("\n")
    assert rule.get_job_blocks(workflow_lines) == expected_eof


def test_get_block_job_not_last_block(
    rule, correct_workflow_name_end, incorrect_workflow_name_end
):
    expected_correct = [
        "  job-name:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test1",
        "",
    ]
    expected_incorrect = [
        "  job-name:",
        "    runs-on: ubuntu-22.04",
        "    steps:",
        "      - run: echo test1",
    ]

    workflow_lines = correct_workflow_name_end.split("\n")
    assert rule.get_job_blocks(workflow_lines) == expected_correct

    workflow_lines = incorrect_workflow_name_end.split("\n")
    assert rule.get_job_blocks(workflow_lines) == expected_incorrect


def test_is_indetion_correct(rule):
    correct_indentation_one = """\
jobs:
  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1
"""

    correct_indentation_two = """\
jobs:

  first-job:
    runs-on: ubuntu-22.04
    steps:
      - run: echo test1
"""

    incorrect_indentation = """\
jobs:
    first-job:
        runs-on: ubuntu-22.04
        steps:
            - run: echo test1
"""

    assert rule.is_indentation_correct(correct_indentation_one.split("\n")) is True
    assert rule.is_indentation_correct(correct_indentation_two.split("\n")) is True
    assert rule.is_indentation_correct(incorrect_indentation.split("\n")) is False

    obj = FileFormat(incorrect_indentation)
    result, message = rule.fn(obj)
    assert result is False
    assert "Dependent YAML indentation is incorrect" in message


def test_rule_on_correct_workflow_single_job(rule, correct_workflow_single_job):
    obj = FileFormat(correct_workflow_single_job)

    result, message = rule.fn(obj)
    assert result is True


def test_rule_on_correct_workflow_multi_job(rule, correct_workflow_multi_job):
    obj = FileFormat(correct_workflow_multi_job)

    result, message = rule.fn(obj)
    assert result is True


def test_rule_on_incorrect_workflow_single_job(rule, incorrect_workflow_single_job):
    obj = FileFormat(incorrect_workflow_single_job)

    result, message = rule.fn(obj)
    assert result is False
    assert "no newline between" in message


def test_rule_on_incorrect_workflow_multi_job(rule, incorrect_workflow_multi_job):
    obj = FileFormat(incorrect_workflow_multi_job)

    result, message = rule.fn(obj)
    assert result is False
    assert "Missing newline prior" in message
