import typing

import yaml
from schema import Schema, SchemaError, Or  # type: ignore
import logging

logger = logging.getLogger("BuildTaskManager")

tasks_schema = Schema({"tasks": [{"name": str, "dependencies": Or(list[str], [])}]})


def read_tasks() -> list[dict[str, typing.Union[str, list[str]]]]:
    tasks_file = "tasks.yaml"
    tasks = read_tasks_yaml(tasks_file)
    return tasks["tasks"]


def read_tasks_yaml(tasks_file):
    with open(tasks_file, "r", encoding="utf-8") as f:
        tasks = yaml.load(f, Loader=yaml.FullLoader)
        try:
            tasks_schema.validate(tasks)
        except SchemaError as e:
            logger.error(e)
            raise RuntimeError(f"{tasks_file} has invalid format")
    return tasks
