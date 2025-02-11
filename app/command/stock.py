import asyncio
from datetime import datetime
from decimal import Decimal

from rich.console import Console
from rich.table import Table
from typer import Typer

from app.service import stock as stock_service

app = Typer(name="stock", help="Stock tools.")
console = Console()


@app.command("get", help="Get stock data by ticker.")
def get_stoke(ticker: str):
    """
    Get stock data by ticker.

    Args:
        ticker (str): Ticker symbol of the stock.
    """
    stoke = asyncio.run(stock_service.get_stock(ticker=ticker.strip()))
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


@app.command("list", help="List stocks by tickers.")
def list_stokes(tickers: list[str]):
    """
    List stocks.

    Args:
        tickers (list[str]): List of ticker symbols of the stocks.
    """
    stokes = asyncio.run(stock_service.list_stocks(tickers=tickers))
    table = Table(box=None)
    for key in stokes[0].__dict__.keys():
        if key != "description":
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


@app.command("most_popular", help="List most popular stocks.")
def get_stokes_most_popular():
    """
    List most popular stocks.
    """
    stokes = asyncio.run(stock_service.list_stocks_most_popular())
    table = Table(box=None)
    for key in ["order"] + list(stokes[0].__dict__.keys()):
        if key != "description":
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
