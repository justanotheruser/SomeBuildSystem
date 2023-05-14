import logging

import click

logger = logging.getLogger("BuildTaskManager")


@click.group()
def cli():
    pass


@click.command(name="list")
def list_command(**kwargs):
    """Show names of loaded builds/tasks"""
    pass


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
