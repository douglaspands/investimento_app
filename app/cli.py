from typer import Typer

from app.command.reit import app as reit_app
from app.command.stock import app as stock_app


def create_app():
    app = Typer(name="investiments", help="CLI for investiments.")
    app.add_typer(stock_app)
    app.add_typer(reit_app)
    return app
