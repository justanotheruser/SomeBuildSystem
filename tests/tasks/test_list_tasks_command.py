import re

import pytest
from click.testing import CliRunner

from build_task_manager.app import list_command


def test_tasks_file_not_found():
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
    assert result.exit_code == 1
    assert result.output == "Could not open tasks file\n"


def test_invalid_input(with_invalid_schema_tasks_file):
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
    assert result.exit_code == 1
    assert re.match(r".*\.yaml has invalid format[\r\n]+", result.output)


@pytest.mark.with_file_in_cwd_from_data("tasks/valid_tasks.yaml", "tasks.yaml")
def test_valid_input(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
    assert result.exit_code == 0
    assert (
        result.output == "List of available tasks:\n"
        " * bring_black_leprechauns\n"
        " * bring_gray_cyclops\n"
        " * bring_green_cyclops\n"
        " * bring_purple_leprechauns\n"
        " * bring_yellow_cyclops\n"
        " * build_blue_leprechauns\n"
        " * build_lime_cyclops\n"
        " * coloring_green_cyclops\n"
        " * create_green_cyclops\n"
        " * create_white_cyclops\n"
        " * design_black_centaurs\n"
        " * design_olive_cyclops\n"
        " * design_silver_cyclops\n"
        " * design_teal_cyclops\n"
        " * enable_fuchsia_fairies\n"
        " * enable_white_cyclops\n"
        " * enable_yellow_cyclops\n"
        " * map_black_cyclops\n"
        " * map_gray_centaurs\n"
        " * read_aqua_cyclops\n"
        " * read_blue_witches\n"
        " * read_lime_cyclops\n"
        " * read_purple_centaurs\n"
        " * train_silver_centaurs\n"
        " * train_white_cyclops\n"
        " * upgrade_blue_centaurs\n"
        " * upgrade_lime_leprechauns\n"
        " * upgrade_olive_gnomes\n"
        " * upgrade_olive_leprechauns\n"
        " * write_aqua_leprechauns\n"
        " * write_lime_leprechauns\n"
    )


@pytest.mark.with_file_in_cwd_from_data("tasks/missing_tasks.yaml", "tasks.yaml")
def test_missing_tasks(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
    assert result.exit_code == 1
    assert (
        result.output == "Following tasks a missing:\n"
        " * task_f: task_c, task_e, task_g depend on it\n"
        " * task_k: task_d, task_g depend on it\n"
        " * task_l: task_d depends on it\n"
        " * task_m: task_d depends on it\n"
    )
