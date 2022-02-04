from lint import lint

def test_lint(capfd):
    file_path = "test.yml"
    lint_output = lint(file_path)
    out, err = capfd.readouterr()
    assert "Step 1 of job key 'download-latest' uses an outdated action, consider updating it" in out
    assert "Run in step 2 of job key 'download-latest' should be a single line." in out
