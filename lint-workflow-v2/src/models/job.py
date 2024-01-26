"""Representation for a job in a GitHub Action workflow."""

from dataclasses import dataclass, field
from typing import List, Optional, Self

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from src.models.step import Step


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Job:
    """Represents a job in a GitHub Action workflow.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requies a key that is missing, the attribute should
    be added to this class to make it available for use in linting.
    """

    runs_on: str = field(metadata=config(field_name="runs-on"))
    key: Optional[str] = None
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    steps: Optional[List[Step]] = None

    @classmethod
    def init(cls: Self, key: str, data: CommentedMap) -> Self:
        """Custom dataclass constructor to map job data to a Job."""
        new_job = cls.from_dict(data)
        new_job.key = key

        return new_job
