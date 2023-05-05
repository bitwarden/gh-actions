from dataclasses import dataclass, field

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from src.models.job import Job


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Workflow:
    name: str = None
    on: CommentedMap = None
    jobs: CommentedMap = None
