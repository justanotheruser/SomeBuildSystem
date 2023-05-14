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
def with_tasks_file(request):
    marker = request.node.get_closest_marker("with_tasks_file_named")
    tasks_file_name = marker.args[0]
    src = f"tests/data/tasks/{tasks_file_name}"
    dst = os.path.join(os.getcwd(), "tasks.yaml")
    shutil.copyfile(src, dst)
    yield
    os.remove(dst)
