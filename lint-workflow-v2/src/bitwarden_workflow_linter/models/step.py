"""Representation for a job step in a GitHub Action workflow."""

from dataclasses import dataclass, field
from typing import Optional, Self

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Step:
    """Represents a step in a GitHub Action workflow job.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requires a key that is missing, the attribute should
    be added to this class to make it available for use in linting.
    """

    key: Optional[int] = None
    job: Optional[str] = None
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    uses: Optional[str] = None
    uses_path: Optional[str] = None
    uses_ref: Optional[str] = None
    uses_comment: Optional[str] = None
    uses_version: Optional[str] = None
    uses_with: Optional[CommentedMap] = field(
        metadata=config(field_name="with"), default=None
    )
    run: Optional[str] = None

    @classmethod
    def init(cls: Self, idx: int, job: str, data: CommentedMap) -> Self:
        """Custom dataclass constructor to map a job step data to a Step."""
        new_step = cls.from_dict(data)

        new_step.key = idx
        new_step.job = job

        if "uses" in data.ca.items and data.ca.items["uses"][2]:
            new_step.uses_comment = data.ca.items["uses"][2].value.replace("\n", "")
            if "@" in new_step.uses:
                new_step.uses_path, new_step.uses_ref = new_step.uses.split("@")
                new_step.uses_version = new_step.uses_comment.split(" ")[-1]

        return new_step
