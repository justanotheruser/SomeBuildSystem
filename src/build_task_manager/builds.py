import logging
import typing
from dataclasses import dataclass

import yaml
from schema import Schema, SchemaError, Or  # type: ignore

from build_task_manager.tasks import Task, Tasks

logger = logging.getLogger("BuildTaskManager")

builds_schema = Schema({"builds": [{"name": str, "tasks": Or(list[str], [])}]})


@dataclass
class Build:
    name: str
    tasks: list[Task]


def read_builds() -> dict[str, dict[str, typing.Union[str, list[str]]]]:
    """Returns dictionary of builds by name"""
    builds_file = "builds.yaml"
    build_list = read_builds_yaml(builds_file)
    builds: dict[str, dict[str, typing.Union[str, list[str]]]] = dict()
    for build in build_list:
        builds[build["name"]] = build  # type: ignore
    return builds


def read_builds_yaml(builds_file: str) -> list[dict[str, typing.Union[str, list[str]]]]:
    with open(builds_file, "r", encoding="utf-8") as f:
        builds = yaml.load(f, Loader=yaml.FullLoader)
        try:
            builds_schema.validate(builds)
        except SchemaError as e:
            logger.error(e)
            raise RuntimeError(f"{builds_file} has invalid format")
    return builds["builds"]


def get_build(build_name: str, tasks: Tasks):
    pass
