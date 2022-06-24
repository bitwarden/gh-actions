from lint import workflow_files


def test_workflow_files():
    assert workflow_files("") == []
    assert workflow_files("test.yml") == ["test.yml"]
    assert workflow_files("test.yml test-alt.yml") == sorted(
        ["test.yml", "test-alt.yml"]
    )
    assert workflow_files("../tests") == sorted(
        ["../tests/test.yml", "../tests/test-alt.yml", "../tests/test_a.yaml"]
    )
    assert workflow_files("test.yml ./") == sorted(
        [".//test-alt.yml", ".//test.yml", ".//test_a.yaml", "test.yml"]
    )
    assert workflow_files("not-a-real-file.yml") == []
