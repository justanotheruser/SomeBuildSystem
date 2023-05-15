import os
import shutil
from contextlib import contextmanager

import pytest


@pytest.fixture(
    params=[
        "tasks/invalid_schema/not_tasks.yaml",
        "tasks/invalid_schema/task_missing_dependencies.yaml",
        "tasks/invalid_schema/task_without_name.yaml",
        "tasks/invalid_schema/unexpected_task_field.yaml",
    ]
)
def with_invalid_schema_tasks_file(request):
    with data_file_in_cwd([request.param], ["tasks.yaml"]):
        yield


@pytest.fixture(
    params=[
        "builds/invalid_schema/not_builds.yaml",
        "builds/invalid_schema/build_without_name.yaml",
    ]
)
def with_invalid_schema_builds_file(request):
    with data_file_in_cwd([request.param], ["builds.yaml"]):
        yield


@pytest.fixture()
def with_file_in_cwd(request):
    marker = request.node.get_closest_marker("with_file_in_cwd_from_data")
    if isinstance(marker.args[0], str):
        with data_file_in_cwd([marker.args[0]], [marker.args[1]]):
            yield
    else:
        with data_file_in_cwd(marker.args[0], marker.args[1]):
            yield


@contextmanager
def data_file_in_cwd(src_file_path_list: list[str], dst_file_name_list: list[str]):
    for src_file_path, dst_file_name in zip(src_file_path_list, dst_file_name_list):
        src = f"tests/data/{src_file_path}"
        shutil.copyfile(src, dst_file_name)
    try:
        yield
    except Exception:
        pass
    finally:
        for dst_file_name in dst_file_name_list:
            os.remove(dst_file_name)
