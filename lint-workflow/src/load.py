from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .models.job import Job
from .models.step import Step
from .models.workflow import Workflow


yaml = YAML()


def load_workflow(filename: str) -> CommentedMap:
    with open(filename) as file:
        return yaml.load(file)


def build_workflow(loaded_yaml: str) -> Workflow:
    return Workflow.from_dict({
        **loaded_yaml,
        "jobs": {str(job_key): Job.from_dict({
            **job,
            "steps": [Step.from_dict(step) for step in job["steps"]]
        }) for job_key, job in loaded_yaml["jobs"].items()}
    })


def get_workflow(filename: str) -> Workflow:
    return build_workflow(load_workflow(filename))


"""
workflow = load_workflow("tests/fixtures/test.yml")
workflow["jobs"]["crowdin-pull"]["steps"][0]._yaml_comment  # has the comment in it
"""
