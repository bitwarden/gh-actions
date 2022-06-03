from lint import lint

def test_lint(capfd):
    file_path = "test.yml"
    lint_output = lint(file_path)
    out, err = capfd.readouterr()
    assert "warning Step 1 of job key 'crowdin-pull' uses an outdated action, consider updating it" in out
    assert "error Step 2 of job key 'crowdin-pull' uses an non-existing action: Azure/logi@77f1b2e3fb80c0e8645114159d17008b8a2e475a." in out
