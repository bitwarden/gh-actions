from dataclasses import dataclass, field

from dataclasses_json import config, dataclass_json
from ruamel.yaml.comments import CommentedMap

from src.models.job import Job


@dataclass_json
@dataclass
class Workflow:
    name: str = None
    on: CommentedMap = None
    jobs: CommentedMap = None
