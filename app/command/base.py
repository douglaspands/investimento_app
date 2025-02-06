from rich.console import Console
from typer import Typer

from app.config import get_config

app = Typer(name="reit", help="REITs utils.")
console = Console()


def _get_version():
    config = get_config()
    console.print(f"v{config.version}")


def init_app(app: Typer):
    app.command("version", help="Show version.")(_get_version)
