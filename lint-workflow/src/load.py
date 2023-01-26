from ruamel.yaml import YAML

from .models.job import Job
from .models.step import Step
from .models.workflow import Workflow


yaml = YAML()


def load_workflow(filename: str) -> Workflow:
    with open(filename) as file:
        #workflow = sanitize_yaml(file.read())
        workflow = yaml.load(file)

    return Workflow(**{
        **workflow,
        "jobs": {str(job_key): Job(**{
            **job,
            "steps": [Step(**step) for step in job["steps"]]
        }) for job_key, job in workflow["jobs"].items()}
    })
