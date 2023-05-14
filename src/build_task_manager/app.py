import logging

import click

from build_task_manager.tasks import read_tasks

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
    except RuntimeError as e:
        click.echo(e)
        return
    click.echo("List of available tasks:")
    for task in tasks:
        click.echo(f' * {task["name"]}')


@list_command.command(name="builds")
def list_builds_command(**kwargs):
    """Show names of loaded builds"""
    click.echo("List of available builds:")


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
    cli.add_command(list_command)
    cli()


if __name__ == "__main__":
    main()
