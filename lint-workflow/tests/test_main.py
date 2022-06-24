from lint import main

# Tests for argparse inputs and outputs using capsys.readouterr()


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


def test_main_folder_and_files(capsys):
    main(["test.yml ./"])
    captured = capsys.readouterr()
    result = captured.out
    print(result)


def test_main_not_found(capsys):
    # File that doesn't exist
    main(["not-a-real-file.yml"])
    captured = capsys.readouterr()
    result = captured.out
    assert isinstance(result, str)
    assert (
        'File(s)/Directory: "not-a-real-file.yml" does not exist, exiting.' in result
    )
    # Empty string
    main([""])
    captured = capsys.readouterr()
    result = captured.out
    assert isinstance(result, str)
    assert 'File(s)/Directory: "" does not exist, exiting.' in result
    # Spaces in string
    main(["  "])
    captured = capsys.readouterr()
    result = captured.out
    assert isinstance(result, str)
    assert 'File(s)/Directory: "  " does not exist, exiting.' in result
