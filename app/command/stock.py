from datetime import datetime
from decimal import Decimal
from typing import Annotated
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.table import Table
from typer import Argument, Option, Typer

from app.command.complete.ticker import complete_stock_tickers
from app.common import aio
from app.config import get_config
from app.enum.scraping import StockScrapingOriginEnum
from app.service import stock as stock_service

app = Typer(name="stock", help="Stock tools.")
console = Console()


@app.command("get", help="Get stock data by ticker.")
def get_stoke(
    ticker: Annotated[
        str, Argument(help="Stock ticker.", autocompletion=complete_stock_tickers)
    ],
    origin: Annotated[
        StockScrapingOriginEnum, Option(help="Data origin.")
    ] = StockScrapingOriginEnum.STATUS_INVEST,
):
    """Get stock data by ticker.

    Args:
        ticker (str): Ticker symbol of the stock.
        origin (StockScrapingOriginEnum, optional): Data origin. Defaults to "Data origin".
    """
    stoke = aio.run(stock_service.get_stock(ticker=ticker.strip(), origin=origin))
    table = Table(box=None)
    for key in ["field", "value"]:
        table.add_column(key.upper())
    for key, value in stoke.__dict__.items():
        table.add_row(
            key.upper(),
            value.astimezone(ZoneInfo(get_config().timezone_local)).isoformat()[:19]
            if isinstance(value, datetime)
            else (f"{value:.2f}" if isinstance(value, Decimal) else str(value)),
        )
    console.print(table)


@app.command("list", help="List stocks by tickers.")
def list_stokes(
    tickers: Annotated[
        list[str], Argument(help="Stock ticker.", autocompletion=complete_stock_tickers)
    ],
    origin: Annotated[
        StockScrapingOriginEnum, Option(help="Data origin.")
    ] = StockScrapingOriginEnum.STATUS_INVEST,
):
    """
    List stocks.

    Args:
        tickers (list[str]): List of ticker symbols of the stocks.
        origin (StockScrapingOriginEnum, optional): Data origin. Defaults to "Data origin".
    """
    stokes = aio.run(stock_service.list_stocks(tickers=tickers, origin=origin))
    table = Table(box=None)
    for key in stokes[0].__dict__.keys():
        if key in ("description", "origin"):
            continue
        if key in ("price",):
            table.add_column(key.upper(), justify="right")
        else:
            table.add_column(key.upper())
    for item in stokes:
        table.add_row(
            *[
                value.astimezone(ZoneInfo(get_config().timezone_local)).isoformat()[:19]
                if isinstance(value, datetime)
                else (f"{value:.2f}" if isinstance(value, Decimal) else str(value))
                for key, value in item.__dict__.items()
                if key not in ("description", "origin")
            ]
        )
    console.print(table)


@app.command("most_popular", help="List most popular stocks.")
def get_stokes_most_popular(
    origin: Annotated[
        StockScrapingOriginEnum, Option(help="Data origin.")
    ] = StockScrapingOriginEnum.STATUS_INVEST,
):
    """
    List most popular stocks.
    Args:
        origin (StockScrapingOriginEnum, optional): Data origin. Defaults to "Data origin".
    """
    stokes = aio.run(stock_service.list_stocks_most_popular(origin=origin))
    table = Table(box=None)
    for key in ["order"] + list(stokes[0].__dict__.keys()):
        if key in ("description", "origin"):
            continue
        if key in ("order", "price"):
            table.add_column(key.upper(), justify="right")
        else:
            table.add_column(key.upper())
    for n, item in enumerate(stokes):
        table.add_row(
            f"{n + 1}",
            *[
                value.astimezone(ZoneInfo(get_config().timezone_local)).isoformat()[:19]
                if isinstance(value, datetime)
                else (f"{value:.2f}" if isinstance(value, Decimal) else str(value))
                for key, value in item.__dict__.items()
                if key not in ("description", "origin")
            ],
        )
    console.print(table)


@app.command("add", help="Add stock data.")
def add_stoke(
    ticker: Annotated[
        str, Option(help="Stock ticker.", autocompletion=complete_stock_tickers)
    ],
    price: Annotated[float, Option(help="Price of stock.")],
    count: Annotated[int, Option(help="Count of stocks.")],
):
    console.print(f"{ticker=} {price=} {count=}")
