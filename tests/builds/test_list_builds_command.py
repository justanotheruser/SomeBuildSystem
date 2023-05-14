import pytest
from click.testing import CliRunner
import re

from build_task_manager.app import list_command


def test_list_builds_invalid_input(with_invalid_schema_builds_file):
    runner = CliRunner()
    result = runner.invoke(list_command, ["builds"])
    assert result.exit_code == 1
    assert re.match(r".*\.yaml has invalid format[\r\n]+", result.output)


@pytest.mark.with_file_in_cwd_from_data("builds/valid_builds.yaml", "builds.yaml")
def test_list_builds_command(with_file_in_cwd):
    runner = CliRunner()
    result = runner.invoke(list_command, ["builds"])
    assert (
        result.output == "List of available builds:\n"
        " * approach_important\n"
        " * audience_stand\n"
        " * time_alone\n"
    )
    assert result.exit_code == 0
