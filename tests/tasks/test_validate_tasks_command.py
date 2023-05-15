import pytest
from click.testing import CliRunner

from build_task_manager.app import validate_command


@pytest.mark.with_file_in_cwd_from_data("tasks/missing_tasks.yaml", "tasks.yaml")
def test_missing_tasks(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(validate_command, ["tasks"])
    assert result.exit_code == 1
    assert (
        result.output == "Following tasks a missing:\n"
        " * task_f: task_c, task_e, task_g depend on it\n"
        " * task_k: task_d, task_g depend on it\n"
        " * task_l: task_d depends on it\n"
        " * task_m: task_d depends on it\n"
    )


@pytest.mark.with_file_in_cwd_from_data("tasks/valid_tasks.yaml", "tasks.yaml")
def test_valid_input(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(validate_command, ["tasks"])
    assert result.exit_code == 0
    assert result.output == "OK\n"
