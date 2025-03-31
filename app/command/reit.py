from datetime import datetime
from decimal import Decimal
from typing import Annotated
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.table import Table
from typer import Argument, Option, Typer

from app.command.complete.ticker import complete_reit_tickers
from app.common import aio
from app.config import get_config
from app.enum.scraping import ReitScrapingOriginEnum
from app.service import reit as reit_service

app = Typer(name="reit", help="REITs tools.")
console = Console()


@app.command("get", help="Get REIT data by ticker.")
def get_reit(
    ticker: Annotated[
        str, Argument(help="REIT ticker.", autocompletion=complete_reit_tickers)
    ],
    origin: Annotated[
        ReitScrapingOriginEnum, Option(help="Data origin.")
    ] = ReitScrapingOriginEnum.STATUS_INVEST,
):
    """
    Get REIT data by ticker.

    Args:
        ticker (str): Ticker symbol of the REIT.
        origin (ReitScrapingOriginEnum, optional): Data origin. Defaults to "Data origin".
    """
    stoke = aio.run(reit_service.get_reit(ticker=ticker.strip(), origin=origin))
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


@app.command("list", help="List REITs by tickers.")
def list_stokes(
    tickers: Annotated[
        list[str], Argument(help="REIT ticker.", autocompletion=complete_reit_tickers)
    ],
    origin: Annotated[
        ReitScrapingOriginEnum, Option(help="Data origin.")
    ] = ReitScrapingOriginEnum.STATUS_INVEST,
):
    """
    List REITs.

    Args:
        tickers (list[str]): List of ticker symbols of the REITs.
        origin (ReitScrapingOriginEnum, optional): Data origin. Defaults to "Data origin".
    """
    stokes = aio.run(reit_service.list_reits(tickers=tickers, origin=origin))
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


@app.command("most_popular", help="List most popular REITs.")
def get_stokes_most_popular(
    origin: Annotated[
        ReitScrapingOriginEnum, Option(help="Data origin.")
    ] = ReitScrapingOriginEnum.STATUS_INVEST,
):
    """
    List most popular REITs.

    Args:
        origin (ReitScrapingOriginEnum, optional): Data origin. Defaults to "Data origin".
    """
    stokes = aio.run(reit_service.list_reits_most_popular(origin=origin))
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
