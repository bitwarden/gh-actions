"""Representation for an entire GitHub Action workflow."""

from dataclasses import dataclass
from typing import Dict, Optional

from dataclasses_json import dataclass_json, Undefined
from ruamel.yaml.comments import CommentedMap

from src.models.job import Job


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Workflow:
    """Represents an entire workflow in a GitHub Action workflow.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requies a key that is missing, the attribute should
    be added to this class to make it available for use in linting.

    See src/models/job.py for an example if the key in the workflow data does not map
    one-to-one in the model (ex. 'with' => 'uses_with')
    """

    key: str = ""
    name: Optional[str] = None
    on: Optional[CommentedMap] = None
    jobs: Optional[Dict[str, Job]] = None
