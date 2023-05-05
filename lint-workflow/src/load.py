from ruamel.yaml import YAML

from .models.job import Job
from .models.step import Step
from .models.workflow import Workflow


yaml = YAML()


def load_workflow(filename: str) -> Workflow:
    with open(filename) as file:
        #workflow = sanitize_yaml(file.read())
        workflow = yaml.load(file)

    return Workflow.from_dict({
        **workflow,
        "jobs": {str(job_key): Job.from_dict({
            **job,
            "steps": [Step.from_dict(step) for step in job["steps"]]
        }) for job_key, job in workflow["jobs"].items()}
    })
