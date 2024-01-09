import json
import pytest

from .conftest import FIXTURE_DIR
from .context import src

from src.lint import LinterCmd
from src.utils import Settings, LintFinding, LintLevels


@pytest.fixture
def settings():
    return Settings()


def test_get_max_error_level(settings):
    linter = LinterCmd(settings=settings)

    assert linter.get_max_error_level([
        LintFinding(level=LintLevels.WARNING),
        LintFinding(level=LintLevels.WARNING)
    ]) == 1

    assert linter.get_max_error_level([
        LintFinding(level=LintLevels.ERROR),
        LintFinding(level=LintLevels.ERROR)
    ]) == 2

    assert linter.get_max_error_level([
        LintFinding(level=LintLevels.ERROR),
        LintFinding(level=LintLevels.ERROR),
        LintFinding(level=LintLevels.WARNING),
        LintFinding(level=LintLevels.WARNING)
    ]) == 2
