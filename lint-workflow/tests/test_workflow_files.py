import os
from lint import workflow_files


def test_workflow_files():
    assert workflow_files("") == []
    assert workflow_files("not-a-real-file.yml") == []
    assert workflow_files("test.yml") == ["test.yml"]
    # multiple files
    assert workflow_files("test.yml test-alt.yml") == sorted(
        ["test.yml", "test-alt.yml"]
    )
    # directory
    assert workflow_files("../tests") == sorted(set(
        ["../tests/"+file for file in os.listdir("../tests") if file.endswith((".yml", ".yaml"))]
    ))
    # directory and files   
    assert workflow_files("test.yml ../tests") == sorted(set(
        ["test.yml"] + ["../tests/"+file for file in os.listdir("./") if file.endswith((".yml", ".yaml"))]
    ))
