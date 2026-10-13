import subprocess


def test_get_pr_id_cmd():
    inputs = [
        {"commit": "7d46c75af91adbfdfc70689f4d8b3405b26bda6b", "expected": "196"},
        {"commit": "f30be53c2a5b3d61928c0f41a2e25605a9901d6a", "expected": "None"},
        {"commit": "f30be53c2a5b3d61928c0f41a2e25605a9901d6b", "expected": "None"},
    ]

    for input in inputs:
        result = subprocess.run(
            ["python", "src/get_pr_id.py", input["commit"]], stdout=subprocess.PIPE
        )

        assert result.stdout.decode().strip("\n") == input["expected"]
