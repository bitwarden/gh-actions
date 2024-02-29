"""Representation for a job in a GitHub Action workflow."""

from dataclasses import dataclass, field
from typing import List, Optional, Self

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from .step import Step


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Job:
    """Represents a job in a GitHub Action workflow.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requires a key that is missing, the attribute should
    be added to this class to make it available for use in linting.
    """

    runs_on: Optional[str] = field(metadata=config(field_name="runs-on"), default=None)
    key: Optional[str] = None
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    steps: Optional[List[Step]] = None
    uses: Optional[str] = None
    uses_path: Optional[str] = None
    uses_ref: Optional[str] = None
    uses_with: Optional[CommentedMap] = field(
        metadata=config(field_name="with"), default=None
    )

    @classmethod
    def init(cls: Self, key: str, data: CommentedMap) -> Self:
        """Custom dataclass constructor to map job data to a Job."""
        init_data = {
            "key": key,
            "name": data["name"] if "name" in data else None,
            "runs-on": data["runs-on"] if "runs-on" in data else None,
            "env": data["env"] if "env" in data else None,
        }

        new_job = cls.from_dict(init_data)

        if "steps" in data:
            new_job.steps = [
                Step.init(idx, new_job.key, step_data)
                for idx, step_data in enumerate(data["steps"])
            ]
        else:
            new_job.uses = data["uses"].replace("\n", "")
            if "@" in new_job.uses:
                new_job.uses_path, new_job.uses_ref = new_job.uses.split("@")

        return new_job
