from click.testing import CliRunner

from build_task_manager.app import list_command


def test_list_tasks_command(tasks_yaml_in_cwd):
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
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
    assert result.exit_code == 0


def test_list_builds_command():
    runner = CliRunner()
    result = runner.invoke(list_command, ["builds"])
    assert result.output == "List of available builds:\n"
    assert result.exit_code == 0
