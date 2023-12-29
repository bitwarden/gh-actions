from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from src.models.job import Job


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Workflow:
    key: str = ""
    name: Optional[str] = None
    on: Optional[CommentedMap] = None
    jobs: Optional[CommentedMap] = None 
