import os
import shutil

import pytest


@pytest.fixture
def tasks_yaml_in_cwd():
    src = "tests/data/tasks.yaml"
    dst = os.path.join(os.getcwd(), "tasks.yaml")
    shutil.copyfile(src, dst)
    yield
    os.remove(dst)
