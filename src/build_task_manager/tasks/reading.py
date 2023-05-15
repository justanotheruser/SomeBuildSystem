import logging
import sys
import typing

import click
import yaml
from schema import Schema, SchemaError, Or  # type: ignore

TaskDict = dict[str, typing.Union[str, list[str]]]
logger = logging.getLogger("BuildTaskManager")

tasks_schema = Schema({"tasks": [{"name": str, "dependencies": Or(list[str], [])}]})


def read_tasks() -> list[TaskDict]:
    tasks_file = "tasks.yaml"
    try:
        tasks = read_tasks_yaml(tasks_file)
    except OSError as e:
        logger.error(e)
        click.echo("Could not open tasks file")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(e)
        click.echo(e)
        sys.exit(1)
    return tasks


def read_tasks_yaml(tasks_file: str) -> list[TaskDict]:
    with open(tasks_file, "r", encoding="utf-8") as f:
        tasks = yaml.load(f, Loader=yaml.FullLoader)
        try:
            tasks_schema.validate(tasks)
        except SchemaError as e:
            logger.error(e)
            raise RuntimeError(f"{tasks_file} has invalid format")
    return tasks["tasks"]
