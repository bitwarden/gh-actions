from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Step:
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    uses: Optional[str] = None
    run: Optional[str] = None
