import logging
import sys

import click

from build_task_manager.builds import read_builds
from build_task_manager.tasks import read_tasks
from build_task_manager.dependency_cycle_finder import (
    DependencyCycleFinder,
    DependencyNotFoundError,
)

logger = logging.getLogger("BuildTaskManager")


@click.group()
def cli():
    pass


@cli.group(name="list")
def list_command(**kwargs):
    """Show names of loaded builds/tasks"""
    pass


@list_command.command(name="tasks")
def list_tasks_command(**kwargs):
    """Show names of loaded tasks"""
    try:
        tasks = read_tasks()
    except OSError as e:
        logger.error(e)
        click.echo("Could not open tasks file")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(e)
        click.echo(e)
        sys.exit(1)
    click.echo("List of available tasks:")
    for task_name in tasks.list_tasks():
        click.echo(f" * {task_name}")


@list_command.command(name="builds")
def list_builds_command(**kwargs):
    """Show names of loaded builds"""
    try:
        builds = read_builds()
    except OSError as e:
        logger.error(e)
        click.echo("Could not open builds file")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(e)
        click.echo(e)
        sys.exit(1)
    click.echo("List of available builds:")
    for build_name in builds.keys():
        click.echo(f" * {build_name}")


@cli.group(name="get")
def get_command(**kwargs):
    """Show detailed information about build/task"""
    pass


@get_command.command(name="task")
@click.argument("task_name")
def get_task_command(task_name):
    """Show information about task and its dependencies"""
    try:
        tasks = read_tasks()
    except OSError as e:
        logger.error(e)
        click.echo("Could not open tasks file")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(e)
        click.echo(e)
        sys.exit(1)
    if not (task := tasks.get_task(task_name)):
        warning_message = f"No such task: {task_name}"
        logger.warning(warning_message)
        click.echo(warning_message)
        sys.exit(1)
    dependencies = ", ".join(task.dependencies)
    click.echo(
        "Task info:\n" f"* name: {task_name}\n" f"* dependencies: {dependencies}"
    )


# TODO: test for duplicated (ambigous) names in tasks/builds
@get_command.command(name="build")
@click.argument("build_name")
def get_build_command(build_name):
    """Show information about build and its dependencies"""
    try:
        builds = read_builds()
    except OSError as e:
        logger.error(e)
        click.echo("Could not open builds file")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(e)
        click.echo(e)
        sys.exit(1)
    if build_name not in builds.keys():
        warning_message = f"No such build: {build_name}"
        logger.warning(warning_message)
        click.echo(warning_message)
        sys.exit(1)
    try:
        tasks = read_tasks()
    except OSError as e:
        logger.error(e)
        click.echo("Could not open tasks file")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(e)
        click.echo(e)
        sys.exit(1)
    cycle_finder = DependencyCycleFinder(builds[build_name]["tasks"], tasks)
    try:
        dependency_cycle = cycle_finder.find_cycle()
    except DependencyNotFoundError as e:
        error_msg = (
            f"{e.dependency} task is required by build but its definition not found"
        )
        logger.error(e)
        click.echo(error_msg)
        sys.exit(1)
    if dependency_cycle:
        cycle_visualization = " -> ".join(dependency_cycle)
        click.echo(f"Build has dependency cycle: {cycle_visualization}")
        sys.exit(1)
    cycle_finder.get_dependencies()
    """if not (build_name := tasks.get_task(build_name)):
        warning_message = f"No such build: {build_name}"
        logger.warning(warning_message)
        click.echo(warning_message)
        sys.exit(1)
    dependencies = ", ".join(task.dependencies)
    click.echo(
        "Task info:\n" f"* name: {task_name}\n" f"* dependencies: {dependencies}"
    )"""


def setup_file_logger():
    ch = logging.FileHandler("BuildTaskManager.log", encoding="utf-8")
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)


def main():
    logger.setLevel(logging.INFO)
    setup_file_logger()
    cli()


if __name__ == "__main__":
    main()
