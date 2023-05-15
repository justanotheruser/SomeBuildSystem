import re

import pytest
from click.testing import CliRunner

from build_task_manager.app import get_command


def test_tasks_file_not_found():
    runner = CliRunner()
    result = runner.invoke(get_command, ["task", "design_teal_cyclops"])
    assert result.exit_code == 1
    assert result.output == "Could not open tasks file\n"


@pytest.mark.with_file_in_cwd_from_data("tasks/valid_tasks.yaml", "tasks.yaml")
def test_task_not_found(with_file_in_cwd):
    runner = CliRunner()
    unknown_task_name = "unknown_task"
    result = runner.invoke(get_command, ["task", unknown_task_name])
    assert result.exit_code == 1
    assert re.match(f"No such task: {unknown_task_name}\n", result.output)


@pytest.mark.with_file_in_cwd_from_data("tasks/valid_tasks.yaml", "tasks.yaml")
def test_get_existing_task(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(get_command, ["task", "design_teal_cyclops"])
    assert result.exit_code == 0
    assert (
        result.output == "Task info:\n"
        "* name: design_teal_cyclops\n"
        "* dependencies: bring_yellow_cyclops, build_lime_cyclops, create_white_cyclops, map_black_cyclops\n"
    )


@pytest.mark.with_file_in_cwd_from_data(
    "tasks/multiple_definitions_for_task.yaml", "tasks.yaml"
)
def test_get_correctly_defined_task_ignore_multiple_definitions_of_another(
    with_file_in_cwd,
):
    runner = CliRunner()
    result = runner.invoke(get_command, ["task", "task_b"])
    assert result.exit_code == 0
    assert (
        result.output == "Task info:\n"
        "* name: task_b\n"
        "* dependencies: task_c, task_d\n"
    )
