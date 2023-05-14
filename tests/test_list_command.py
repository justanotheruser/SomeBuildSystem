from click.testing import CliRunner

from build_task_manager.app import list_command


def test_list_tasks_command():
    runner = CliRunner()
    result = runner.invoke(list_command, ["tasks"])
    assert result.output == "List of available tasks:\n"
    assert result.exit_code == 0


def test_list_builds_command():
    runner = CliRunner()
    result = runner.invoke(list_command, ["builds"])
    assert result.output == "List of available builds:\n"
    assert result.exit_code == 0
