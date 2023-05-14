import typing

import yaml
from schema import Schema, SchemaError, Or  # type: ignore
import logging

logger = logging.getLogger("BuildTaskManager")

builds_schema = Schema({"builds": [{"name": str, "tasks": Or(list[str], [])}]})


def read_builds() -> list[dict[str, typing.Union[str, list[str]]]]:
    builds_file = "builds.yaml"
    builds = read_builds_yaml(builds_file)
    return builds["builds"]


def read_builds_yaml(builds_file: str):
    with open(builds_file, "r", encoding="utf-8") as f:
        builds = yaml.load(f, Loader=yaml.FullLoader)
        try:
            builds_schema.validate(builds)
        except SchemaError as e:
            logger.error(e)
            raise RuntimeError(f"{builds_file} has invalid format")
    return builds
