import os

from lint import workflow_files
from .configs import FIXTURES_DIR


def test_workflow_files():
    assert workflow_files("") == []
    assert workflow_files("not-a-real-file.yml") == []
    assert workflow_files(f"{FIXTURES_DIR}/test.yml") == [f"{FIXTURES_DIR}/test.yml"]
    # multiple files
    assert workflow_files(
        f"{FIXTURES_DIR}/test.yml {FIXTURES_DIR}/test-alt.yml"
    ) == sorted([f"{FIXTURES_DIR}/test.yml", f"{FIXTURES_DIR}/test-alt.yml"])
    # directory
    assert workflow_files(FIXTURES_DIR) == sorted(
        set(
            [
                f"{FIXTURES_DIR}/{file}"
                for file in os.listdir(FIXTURES_DIR)
                if file.endswith((".yml", ".yaml"))
            ]
        )
    )
    # directory and files
    assert workflow_files(f"{FIXTURES_DIR}/test.yml {FIXTURES_DIR}") == sorted(
        set(
            [f"{FIXTURES_DIR}/test.yml"]
            + [
                f"{FIXTURES_DIR}/{file}"
                for file in os.listdir(FIXTURES_DIR)
                if file.endswith((".yml", ".yaml"))
            ]
        )
    )
