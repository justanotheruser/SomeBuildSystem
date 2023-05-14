from click.testing import CliRunner

from build_task_manager.app import list_command


def test_list_command():
    runner = CliRunner()
    result = runner.invoke(list_command)
    assert result.exit_code == 0
