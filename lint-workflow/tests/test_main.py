from lint import main


def test_main_single_file(capsys):
    main(["test.yml"])
    captured = capsys.readouterr()
    result = captured.out
    assert "test.yml" in result


def test_main_multiple_files(capsys):
    main(["test.yml test-alt.yml"])
    captured = capsys.readouterr()
    result = captured.out
    assert isinstance(result, str)
    assert "test.yml" in result
    assert "test-alt.yml" in result


def test_main_folder(capsys):
    main(["./"])
    captured = capsys.readouterr()
    result = captured.out
    assert isinstance(result, str)
    assert "test.yml" in result
    assert "test-alt.yml" in result


def test_main_not_found(capsys):
    main(["not-a-real-file.yml"])
    captured = capsys.readouterr()
    result = captured.out
    assert isinstance(result, str)
    assert "File(s)/Directory does not exist, exiting." in result
