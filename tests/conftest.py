import os
import shutil

import pytest


@pytest.fixture(
    params=[
        "invalid/unexpected_task_field.yaml",
        "invalid/task_missing_dependencies.yaml",
    ]
)
def with_invalid_tasks_file(request):
    src = f"tests/data/tasks/{request.param}"
    dst = os.path.join(os.getcwd(), "tasks.yaml")
    shutil.copyfile(src, dst)
    yield
    os.remove(dst)


@pytest.fixture()
def with_file_in_cwd(request):
    marker = request.node.get_closest_marker("with_file_in_cwd_from_data")
    src_file_path, dst_file_name = marker.args[0], marker.args[1]
    src = f"tests/data/{src_file_path}"
    dst = os.path.join(os.getcwd(), dst_file_name)
    shutil.copyfile(src, dst)
    yield
    os.remove(dst)
