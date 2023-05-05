from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config, dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from src.models.step import Step

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Job:
    runs_on: str = field(metadata=config(field_name="runs-on"))
    name: str = None
    env: Optional[CommentedMap] = None
    steps: List[Step] = None
