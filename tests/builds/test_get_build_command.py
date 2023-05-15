import re

import pytest
from click.testing import CliRunner

from build_task_manager.app import get_command


def test_builds_file_not_found():
    runner = CliRunner()
    result = runner.invoke(get_command, ["build", "approach_important"])
    assert result.exit_code == 1
    assert re.match("Could not open builds file\n", result.output)


@pytest.mark.with_file_in_cwd_from_data("builds/valid_builds.yaml", "builds.yaml")
def test_build_not_found(with_file_in_cwd):
    runner = CliRunner()
    unknown_task_name = "unknown_build"
    result = runner.invoke(get_command, ["build", unknown_task_name])
    assert result.exit_code == 1
    assert re.match(f"No such build: {unknown_task_name}\n", result.output)


@pytest.mark.with_file_in_cwd_from_data("builds/valid_builds.yaml", "builds.yaml")
def test_tasks_file_not_found(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(get_command, ["build", "approach_important"])
    assert result.exit_code == 1
    assert re.match("Could not open tasks file\n", result.output)


"""
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
"""
