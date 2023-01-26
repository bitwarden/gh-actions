from pydantic import BaseModel, Extra, Field, validator
from ruamel.yaml.comments import CommentedMap

from src.models.step import Step


class Job(BaseModel, extra=Extra.allow):
    name: str = None
    runs_on: str = Field(..., alias="runs-on")
    env: CommentedMap = None
    needs: list[str] = None
    steps: list[Step] = None

    #@validator('steps')
    #def check_num_steps(cls, value):
    #    if len(value) < 1:
    #        raise ValueError("'jobs' require at least one 'step'")
    #    return value

