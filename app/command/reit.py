import asyncio
from datetime import datetime

from rich.console import Console
from rich.table import Table
from typer import Typer

from app.service.scraping import reit as reit_scraping

app = Typer(name="reit", help="REITs utils")
console = Console()


@app.command("get", help="Get REIT data by ticker.")
def get_reit(ticker: str):
    """
    Get REIT data by ticker.

    Args:
        ticker (str): Ticker symbol of the REIT.
    """
    stoke = asyncio.run(reit_scraping.get_reit(ticker=ticker.strip()))
    table = Table(box=None)
    for key in ["field", "value"]:
        table.add_column(key.upper())
    for key, value in stoke.__dict__.items():
        table.add_row(
            key.upper(),
            value.isoformat() if isinstance(value, datetime) else str(value),
        )
    console.print(table)


@app.command("list", help="List REITs by tickers.")
def list_stokes(tickers: list[str]):
    """
    List REITs.

    Args:
        tickers (list[str]): List of ticker symbols of the REITs.
    """
    stokes = asyncio.run(reit_scraping.list_reits(tickers=tickers))
    if not stokes:
        console.print("Tickers not found.")
        return
    table = Table(box=None)
    for key in stokes[0].__dict__.keys():
        if key != "description":
            table.add_column(key.upper())
    for item in stokes:
        table.add_row(
            *[
                value.isoformat() if isinstance(value, datetime) else str(value)
                for key, value in item.__dict__.items()
                if key != "description"
            ]
        )
    console.print(table)
