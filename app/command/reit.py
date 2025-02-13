import asyncio
from datetime import datetime
from decimal import Decimal

from rich.console import Console
from rich.table import Table
from typer import Typer

from app.service import reit as reit_service

app = Typer(name="reit", help="REITs tools.")
console = Console()


@app.command("get", help="Get REIT data by ticker.")
def get_reit(ticker: str):
    """
    Get REIT data by ticker.

    Args:
        ticker (str): Ticker symbol of the REIT.
    """
    stoke = asyncio.run(reit_service.get_reit(ticker=ticker.strip()))
    table = Table(box=None)
    for key in ["field", "value"]:
        table.add_column(key.upper())
    for key, value in stoke.__dict__.items():
        table.add_row(
            key.upper(),
            value.isoformat()
            if isinstance(value, datetime)
            else (f"{value:.2f}" if isinstance(value, Decimal) else str(value)),
        )
    console.print(table)


@app.command("list", help="List REITs by tickers.")
def list_stokes(tickers: list[str]):
    """
    List REITs.

    Args:
        tickers (list[str]): List of ticker symbols of the REITs.
    """
    stokes = asyncio.run(reit_service.list_reits(tickers=tickers))
    table = Table(box=None)
    for key in stokes[0].__dict__.keys():
        if key == "description":
            continue
        if key in ("price",):
            table.add_column(key.upper(), justify="right")
        else:
            table.add_column(key.upper())
    for item in stokes:
        table.add_row(
            *[
                value.isoformat()
                if isinstance(value, datetime)
                else (f"{value:.2f}" if isinstance(value, Decimal) else str(value))
                for key, value in item.__dict__.items()
                if key != "description"
            ]
        )
    console.print(table)


@app.command("most_popular", help="List most popular REITs.")
def get_stokes_most_popular():
    """
    List most popular REITs.
    """
    stokes = asyncio.run(reit_service.list_reits_most_popular())
    table = Table(box=None)
    for key in ["order"] + list(stokes[0].__dict__.keys()):
        if key == "description":
            continue
        if key in ("order", "price"):
            table.add_column(key.upper(), justify="right")
        else:
            table.add_column(key.upper())

    for n, item in enumerate(stokes):
        table.add_row(
            f"{n + 1}",
            *[
                value.isoformat()
                if isinstance(value, datetime)
                else (f"{value:.2f}" if isinstance(value, Decimal) else str(value))
                for key, value in item.__dict__.items()
                if key != "description"
            ],
        )
    console.print(table)
