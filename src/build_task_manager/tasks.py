import logging
import typing
from dataclasses import dataclass

import yaml
from schema import Schema, SchemaError, Or  # type: ignore

logger = logging.getLogger("BuildTaskManager")

tasks_schema = Schema({"tasks": [{"name": str, "dependencies": Or(list[str], [])}]})


@dataclass
class Task:
    name: str
    dependencies: list[str]


class Tasks:
    def __init__(self):
        self.tasks = dict()

    def add(self, task_dict: dict):
        task_name = task_dict["name"]
        self.tasks[task_name] = Task(
            name=task_name, dependencies=sorted(task_dict["dependencies"])
        )

    def find_missing_tasks(self) -> dict[str, list[str]]:
        """Returns dictionary that maps missing tasks to list of tasks which declared them as a dependency."""
        missing_tasks: dict[str, list[str]] = dict()
        for name, task in self.tasks.items():
            for dependency in task.dependencies:
                if dependency not in self.tasks:
                    if dependency not in missing_tasks:
                        missing_tasks[dependency] = []
                    missing_tasks[dependency].append(name)
        return missing_tasks

    def list_tasks(self) -> list[str]:
        """Returns sorted list of task names"""
        return sorted(self.tasks.keys())

    def get_task(self, name: str) -> typing.Optional[Task]:
        """Return task if it exists or None otherwise"""
        if name not in self.tasks.keys():
            return None
        return self.tasks[name]


def read_tasks() -> Tasks:
    tasks_file = "tasks.yaml"
    tasks_list = read_tasks_yaml(tasks_file)
    tasks = Tasks()
    for task_dict in tasks_list:
        tasks.add(task_dict)
    if missing_tasks := tasks.find_missing_tasks():
        error_msg = get_missing_tasks_error_message(missing_tasks)
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    return tasks


def read_tasks_yaml(tasks_file: str) -> list[dict[str, typing.Union[str, list[str]]]]:
    with open(tasks_file, "r", encoding="utf-8") as f:
        tasks = yaml.load(f, Loader=yaml.FullLoader)
        try:
            tasks_schema.validate(tasks)
        except SchemaError as e:
            logger.error(e)
            raise RuntimeError(f"{tasks_file} has invalid format")
    return tasks["tasks"]


def get_missing_tasks_error_message(missing_tasks: dict[str, list[str]]) -> str:
    """Returns message about each missing task and tasks that depend on it.
    Tasks are sorted by name, and dependencies of each task are also sorted."""
    assert missing_tasks
    result = "Following tasks a missing:\n"
    lines: list[tuple[str, list[str]]] = []
    for task, depend_on_it in missing_tasks.items():
        lines.append((task, sorted(depend_on_it)))
    lines.sort(key=lambda x: x[0])
    for line in lines:
        dependent_tasks_names = ", ".join(line[1])
        depend_verb = "depend" if len(line[1]) > 1 else "depends"
        result += f" * {line[0]}: {dependent_tasks_names} {depend_verb} on it\n"
    return result[:-1]
