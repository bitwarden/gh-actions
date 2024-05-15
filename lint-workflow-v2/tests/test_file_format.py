"""Test src/bitwarden_workflow_linter/models/workflow.py."""

import pytest

from src.bitwarden_workflow_linter.models.file_format import FileFormat


@pytest.fixture(name="simple_workflow_yaml")
def fixture_simple_workflow_yaml():
    return """\
---
name: test
on:
  workflow_dispatch:

jobs:
  job-key:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: echo test
"""


@pytest.fixture(name="complex_workflow_yaml")
def fixture_complex_workflow_yaml():
    return """\
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


def test_simple_workflow(simple_workflow_yaml):
    file = FileFormat(simple_workflow_yaml)

    assert len(file.lines) == 13


def test_complex_workflow(complex_workflow_yaml):
    file = FileFormat(complex_workflow_yaml)

    assert len(file.lines) == 34
