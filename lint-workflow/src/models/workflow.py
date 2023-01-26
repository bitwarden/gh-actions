from pydantic import BaseModel, Extra
from ruamel.yaml.comments import CommentedMap

from src.models.job import Job


class Workflow(BaseModel, extra=Extra.allow):
    name: str = None
    on: CommentedMap = None
    jobs: CommentedMap = None
