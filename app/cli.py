from typer import Typer

from app.command.main import init_app as command_init_app
from app.command.reit import app as reit_app
from app.command.stock import app as stock_app
from app.command.utils import app as utils_app
from app.config import get_config
from app.infra import migration


def create_app():
    config = get_config()
    migration.upgrade_head()
    app = Typer(
        name="investiments",
        help=f"{config.description}. < v{config.version} >",
        rich_markup_mode="rich",
        context_settings={"help_option_names": ["-h", "--help"]},
        add_completion=False,
        no_args_is_help=True,
    )
    command_init_app(app)
    app.add_typer(stock_app, rich_help_panel="Investiments")
    app.add_typer(reit_app, rich_help_panel="Investiments")
    app.add_typer(utils_app, rich_help_panel="Tools and Utils")
    return app
