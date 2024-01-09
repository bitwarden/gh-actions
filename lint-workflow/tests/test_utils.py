import json
import pytest

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .conftest import FIXTURE_DIR
from .context import src

from src.utils import Action, Colors, LintFinding, LintLevels


def test_action_eq():
    action_def = {"name": "bitwarden/sm-action", "version": "1.0.0", "sha": "some-sha"}

    action_a = Action(**action_def)
    action_b = Action(**action_def)

    assert (action_a == action_b) == True
    assert (action_a != action_b) == False


def test_action_ne():
    action_a = Action(name="bitwarden/sm-action", version="1.0.0", sha="some-sha")
    action_b = Action(name="bitwarden/sm-action", version="1.1.0", sha="some-other-sha")

    assert (action_a == action_b) == False
    assert (action_a != action_b) == True


def test_lint_level():
    warning = LintLevels.WARNING
    assert warning.code == 1
    assert warning.color == Colors.yellow


def test_lint_finding():
    warning = LintFinding(level=LintLevels.WARNING)
    assert str(warning) == "\x1b[33mwarning\x1b[0m <no description>"

    error = LintFinding(level=LintLevels.ERROR)
    assert str(error) == "\x1b[31merror\x1b[0m <no description>"
