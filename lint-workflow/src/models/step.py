from dataclasses import dataclass, field
from typing import Optional, Self

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Step:
    key: Optional[int] = None
    job: Optional[str] = None
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    uses: Optional[str] = None
    uses_comment: Optional[str] = None
    uses_with: Optional[CommentedMap] = field(metadata=config(field_name="with"), default=None)
    run: Optional[str] = None

    @classmethod
    def init(cls, idx: int, job: str, data: CommentedMap) -> Self:
        new_step = cls.from_dict(data)

        new_step.key = idx
        new_step.job = job

        if "uses" in data.ca.items and data.ca.items["uses"][2]:
            new_step.uses_comment = data.ca.items["uses"][2].value.replace('\n', '')

        return new_step