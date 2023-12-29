import importlib
from typing import List

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .models.job import Job
from .models.step import Step
from .models.workflow import Workflow
from .rule import Rule


yaml = YAML()


class WorkflowBuilder:
    @classmethod
    def __load_workflow(cls, filename: str) -> CommentedMap:
        with open(filename) as file:
            return yaml.load(file)

    @classmethod
    def __build_workflow(cls, loaded_yaml: str) -> Workflow:
        return Workflow.from_dict({
            **loaded_yaml,
            "jobs": {str(job_key): Job.init(job_key, {
                **job,
                "steps": [
                    Step.init(idx, job_key, step_data)
                    for idx, step_data in enumerate(job["steps"])
                ]
            }) for job_key, job in loaded_yaml["jobs"].items()}
        })

    @classmethod
    def build(cls, filename: str) -> Workflow:
        return cls.__build_workflow(cls.__load_workflow(filename))


class Rules:
    workflow: List[Rule] = []
    job: List[Rule] = []
    step: List[Rule] = []

    def __init__(self, settings: List[str], verbose: bool = False) -> None:
        for rule in settings:
            module_name = rule.split('.')
            module_name = ".".join(module_name[:-1])
            rule_name = rule.split('.')[-1]

            try:
                rule_module = getattr(importlib.import_module(module_name), rule_name)
                rule_inst = rule_module()

                if Workflow in rule_inst.compatibility:
                    self.workflow.append(rule_inst)
                if Job in rule_inst.compatibility:
                    self.job.append(rule_inst)
                if Step in rule_inst.compatibility:
                    self.step.append(rule_inst)
            except Error:
                print(f"Error loading: {rule}\n{Error}")

        if verbose:
            print("===== Loaded Rules =====")
            print("workflow rules:")
            for rule in self.workflow:
                print(f" - {type(rule).__name__}")
            print("job rules:")
            for rule in self.job:
                print(f" - {type(rule).__name__}")
            print("step rules:")
            for rule in self.step:
                print(f" - {type(rule).__name__}")
            print("========================\n")