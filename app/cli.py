from typer import Typer

from app.command.base import init_app as command_init_app
from app.command.reit import app as reit_app
from app.command.stock import app as stock_app
from app.config import get_config
from app.infra.migration import migration_upgrade_head


def create_app():
    migration_upgrade_head()
    config = get_config()
    app = Typer(
        name="investiments",
        help=f"{config.description}. < v{config.version} >",
        add_completion=False,
    )
    command_init_app(app)
    app.add_typer(stock_app)
    app.add_typer(reit_app)
    return app
