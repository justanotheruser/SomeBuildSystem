black src
black tests
flake8
mypy --config-file pyproject.toml
coverage run -m pytest tests