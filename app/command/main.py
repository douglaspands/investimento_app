import typer
from rich.console import Console
from typer import Typer

from app.config import get_config


def _get_version(option_enabled: bool):
    if option_enabled:
        console = Console(no_color=True)
        console.print(f"v{get_config().version}")
        raise typer.Exit()


def _add_options(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=_get_version,
        is_eager=True,
        help="Print the version and exit.",
    ),
):
    pass


def init_app(app: Typer):
    app.callback()(_add_options)
