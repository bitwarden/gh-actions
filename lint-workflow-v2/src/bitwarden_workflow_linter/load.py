"""Module to load for Workflows and Rules."""

import importlib

from typing import List, Optional

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .models.job import Job
from .models.step import Step
from .models.workflow import Workflow
from .rule import Rule
from .utils import Settings


yaml = YAML()


class WorkflowBuilderError(Exception):
    """Exception to indicate an error with the WorkflowBuilder."""

    pass


class WorkflowBuilder:
    """Collection of methods to build Workflow objects."""

    @classmethod
    def __load_workflow_from_file(cls, filename: str) -> CommentedMap:
        """Load YAML from disk.

        Args:
          filename:
            The name of the YAML file to read.

        Returns:
          A CommentedMap that contains the dict() representation of the
          YAML file. It includes the comments as a part of their respective
          objects (depending on their location in the file).
        """
        with open(filename, encoding="utf8") as file:
            return yaml.load(file)

    @classmethod
    def __build_workflow(cls, loaded_yaml: CommentedMap) -> Workflow:
        """Parse the YAML and build out the workflow to run Rules against.

        Args:
          loaded_yaml:
            YAML that was loaded from either code or a file

        Returns
          A Workflow to run linting Rules against
        """
        return Workflow.init("", loaded_yaml)

    @classmethod
    def build(
        cls,
        filename: Optional[str] = None,
        workflow: Optional[CommentedMap] = None,
        from_file: bool = True,
    ) -> Workflow:
        """Build a Workflow from either code or a file.

        This is a method that assists in testing by abstracting the disk IO
        and allows for passing in a YAML object in code.

        Args:
          filename:
            The name of the file to load the YAML workflow from
          yaml:
            Pre-loaded YAML of a workflow
          from_file:
            Flag to determine if the YAML has already been loaded or needs to
            be loaded from disk
        """
        if from_file and filename is not None:
            return cls.__build_workflow(cls.__load_workflow_from_file(filename))
        elif not from_file and workflow is not None:
            return cls.__build_workflow(workflow)

        raise WorkflowBuilderError(
            "The workflow must either be built from a file or from a CommentedMap"
        )


class LoadRulesError(Exception):
    """Exception to indicate an error with loading rules."""

    pass


class Rules:
    """A collection of all of the types of rules.

    Rules is used as a collection of which Rules apply to which parts of the
    workflow. It also assists in making sure the Rules that apply to multiple
    types are not skipped.
    """

    workflow: List[Rule] = []
    job: List[Rule] = []
    step: List[Rule] = []

    def __init__(self, settings: Settings) -> None:
        """Initializes the Rules

        Args:
          settings:
            A Settings object that contains any default, overridden, or custom settings
            required anywhere in the application.
        """
        # [TODO]: data resiliency
        for rule in settings.enabled_rules:
            module_name = rule.split(".")
            module_name = ".".join(module_name[:-1])
            rule_name = rule.split(".")[-1]

            try:
                rule_class = getattr(importlib.import_module(module_name), rule_name)
                rule_inst = rule_class(settings=settings)

                if Workflow in rule_inst.compatibility:
                    self.workflow.append(rule_inst)
                if Job in rule_inst.compatibility:
                    self.job.append(rule_inst)
                if Step in rule_inst.compatibility:
                    self.step.append(rule_inst)
            except LoadRulesError as err:
                print(f"Error loading: {rule}\n{err}")

    def list(self) -> None:
        """Print the loaded Rules."""
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
