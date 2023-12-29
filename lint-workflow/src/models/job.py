from dataclasses import dataclass, field
from typing import List, Optional, Self

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from src.models.step import Step

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Job:
    runs_on: str = field(metadata=config(field_name="runs-on"))
    key: Optional[str] = None
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    steps: List[Step] = None

    @classmethod
    def init(cls, key: str, data: CommentedMap) -> Self:
        new_job = cls.from_dict(data)
        new_job.key = key

        return new_job
