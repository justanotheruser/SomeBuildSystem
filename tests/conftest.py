import os
import shutil
from contextlib import contextmanager
import pytest


@pytest.fixture(
    params=[
        "tasks/invalid/not_tasks.yaml",
        "tasks/invalid/task_missing_dependencies.yaml",
        "tasks/invalid/task_without_name.yaml",
        "tasks/invalid/unexpected_task_field.yaml",
    ]
)
def with_invalid_tasks_file(request):
    with data_file_in_cwd(request.param, "tasks.yaml"):
        yield


@pytest.fixture(
    params=["builds/invalid/not_builds.yaml", "builds/invalid/build_without_name.yaml"]
)
def with_invalid_builds_file(request):
    with data_file_in_cwd(request.param, "builds.yaml"):
        yield


@pytest.fixture()
def with_file_in_cwd(request):
    marker = request.node.get_closest_marker("with_file_in_cwd_from_data")
    with data_file_in_cwd(marker.args[0], marker.args[1]):
        yield


@contextmanager
def data_file_in_cwd(src_file_path, dst_file_name):
    src = f"tests/data/{src_file_path}"
    shutil.copyfile(src, dst_file_name)
    yield
    os.remove(dst_file_name)
