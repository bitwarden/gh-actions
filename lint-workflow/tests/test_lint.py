from lint import lint
from .configs import FIXTURES_DIR


def test_lint(capfd):
    file_path = f"{FIXTURES_DIR}/test.yml"
    lint_output = lint(file_path)
    out, err = capfd.readouterr()
    assert (
        "\x1b[33mwarning\x1b[0m Name value for workflow is not capitalized. [crowdin Pull]"
        in out
    )
    assert (
        "\x1b[33mwarning\x1b[0m Step 4 of job key 'crowdin-pull' uses an outdated action, consider updating it"
        in out
    )
    assert (
        "\x1b[31merror\x1b[0m Step 2 of job key 'crowdin-pull' uses an non-existing action: Azure/logi@77f1b2e3fb80c0e8645114159d17008b8a2e475a."
        in out
    )
