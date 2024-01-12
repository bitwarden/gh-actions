"""Test src/lint.py."""
import pytest

from src.lint import LinterCmd
from src.utils import Settings, LintFinding, LintLevels


@pytest.fixture(name="settings")
def fixture_settings():
    return Settings()


def test_get_max_error_level(settings):
    linter = LinterCmd(settings=settings)

    assert (
        linter.get_max_error_level(
            [
                LintFinding(description="", level=LintLevels.WARNING),
                LintFinding(description="", level=LintLevels.WARNING),
            ]
        )
        == 1
    )

    assert (
        linter.get_max_error_level(
            [
                LintFinding(description="", level=LintLevels.ERROR),
                LintFinding(description="", level=LintLevels.ERROR),
            ]
        )
        == 2
    )

    assert (
        linter.get_max_error_level(
            [
                LintFinding(description="", level=LintLevels.ERROR),
                LintFinding(description="", level=LintLevels.ERROR),
                LintFinding(description="", level=LintLevels.WARNING),
                LintFinding(description="", level=LintLevels.WARNING),
            ]
        )
        == 2
    )
