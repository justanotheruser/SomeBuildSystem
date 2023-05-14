import pytest
from click.testing import CliRunner
import re

from build_task_manager.app import list_command


def test_list_tasks_invalid_input(with_invalid_tasks_file):
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
    assert result.exit_code == 1
    assert re.match(r".*\.yaml has invalid format[\r\n]+", result.output)


@pytest.mark.with_file_in_cwd_from_data('tasks/valid_tasks.yaml', 'tasks.yaml')
def test_list_tasks_command(with_file_in_cwd):
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


@pytest.mark.with_file_in_cwd_from_data('builds/valid_builds.yaml', 'builds.yaml')
def test_list_builds_command(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(list_command, ["builds"])
    assert result.output == "List of available builds:\n" \
        " * approach_important\n" \
        " * audience_stand\n" \
        " * time_alone\n"
    assert result.exit_code == 0
