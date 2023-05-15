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
    assert "Could not open tasks file\n" == result.output


@pytest.mark.with_file_in_cwd_from_data(
    [
        "builds/build_with_missing_dependency.yaml",
        "tasks/build_with_missing_dependency_tasks.yaml",
    ],
    ["builds.yaml", "tasks.yaml"],
)
def test_dependency_not_found(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(get_command, ["build", "build_with_missing_dependency"])
    assert result.exit_code == 1
    assert (
        result.output
        == "task_c task is required by build but its definition not found\n"
    )


@pytest.mark.with_file_in_cwd_from_data(
    [
        "builds/build_with_cycle.yaml",
        "tasks/build_with_cycle_tasks.yaml",
    ],
    ["builds.yaml", "tasks.yaml"],
)
def test_build_with_cycle(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(get_command, ["build", "build_with_cycle"])
    assert result.exit_code == 1
    assert (
        result.output
        == "Build has dependency cycle: task_f -> task_c -> task_d -> task_f\n"
    )


@pytest.mark.with_file_in_cwd_from_data(
    [
        "builds/build_with_cycle_2.yaml",
        "tasks/build_with_cycle_2_tasks.yaml",
    ],
    ["builds.yaml", "tasks.yaml"],
)
def test_build_with_cycle_2(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(get_command, ["build", "build_with_cycle_2"])
    assert result.exit_code == 1
    assert result.output == "Build has dependency cycle: task_c -> task_d -> task_c\n"


@pytest.mark.with_file_in_cwd_from_data(
    [
        "builds/valid_builds.yaml",
        "tasks/valid_tasks.yaml",
    ],
    ["builds.yaml", "tasks.yaml"],
)
@pytest.mark.parametrize(
    "build",
    [
        (
            "approach_important",
            "Build info:\n"
            " * name: approach_important\n"
            " * dependencies: map_gray_centaurs, design_black_centaurs, read_purple_centaurs, "
            "train_silver_centaurs, upgrade_blue_centaurs\n",
        ),
        (
            "audience_stand",
            "Build info:\n"
            " * name: audience_stand\n"
            " * dependencies: enable_fuchsia_fairies, read_blue_witches, "
            "upgrade_olive_gnomes\n",
        ),
        (
            "time_alone",
            "Build info:\n"
            " * name: time_alone\n"
            " * dependencies: design_olive_cyclops, upgrade_lime_leprechauns, "
            "bring_black_leprechauns, bring_gray_cyclops, bring_green_cyclops, "
            "bring_purple_leprechauns, bring_yellow_cyclops, build_blue_leprechauns, "
            "build_lime_cyclops, coloring_green_cyclops, create_green_cyclops, "
            "create_white_cyclops, design_silver_cyclops, design_teal_cyclops, "
            "enable_white_cyclops, enable_yellow_cyclops, map_black_cyclops, "
            "read_aqua_cyclops, read_lime_cyclops, train_white_cyclops, "
            "upgrade_olive_leprechauns, write_aqua_leprechauns, write_lime_leprechauns\n",
        ),
    ],
)
def test_valid_build(with_file_in_cwd, build):
    runner = CliRunner()
    result = runner.invoke(get_command, ["build", build[0]])
    assert result.output == build[1]
    assert result.exit_code == 0
