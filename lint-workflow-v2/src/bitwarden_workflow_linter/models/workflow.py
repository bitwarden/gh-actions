"""Representation for an entire GitHub Action workflow."""

from dataclasses import dataclass
from typing import Dict, Optional, Self

from dataclasses_json import dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from .job import Job


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Workflow:
    """Represents an entire workflow in a GitHub Action workflow.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requires a key that is missing, the attribute should
    be added to this class to make it available for use in linting.

    See src/models/job.py for an example if the key in the workflow data does not map
    one-to-one in the model (ex. 'with' => 'uses_with')
    """

    key: str = ""
    name: Optional[str] = None
    on: Optional[CommentedMap] = None
    jobs: Optional[Dict[str, Job]] = None

    @classmethod
    def init(cls: Self, key: str, data: CommentedMap) -> Self:
        init_data = {
            "key": key,
            "name": data["name"] if "name" in data else None,
            "on": data["on"] if "on" in data else None,
        }

        new_workflow = cls.from_dict(init_data)

        new_workflow.jobs = {
            str(job_key): Job.init(job_key, job)
            for job_key, job in data["jobs"].items()
        }

        return new_workflow
