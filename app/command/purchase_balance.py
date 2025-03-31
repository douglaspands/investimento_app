from decimal import Decimal
from typing import Annotated
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.table import Table
from typer import Argument, Option, Typer

from app.command.complete.ticker import complete_reit_tickers, complete_stock_tickers
from app.common import aio
from app.config import get_config
from app.resource.purchase_balance import PurchaseBalance
from app.service import purchase_balance as purchase_balance_service

app = Typer(name="balance", help="Purchase balancing tools.")
console = Console()


@app.command("stock", help="Stock purchase balancing.")
def stock_purchase_balancing(
    tickers: Annotated[
        list[str],
        Argument(help="Stock tickers.", autocompletion=complete_stock_tickers),
    ],
    amount: Annotated[float, Option(help="Amount invested.")],
):
    purchase_balance: PurchaseBalance = aio.run(
        purchase_balance_service.stock_purchase_balancing(
            tickers=tickers, amount_invested=Decimal(str(amount))
        )
    )
    table_detail = Table(box=None)
    for key in ("ticket", "price", "count", "total", "updated_at"):
        if key in ("price", "total", "count"):
            table_detail.add_column(key.upper(), justify="right")
        else:
            table_detail.add_column(key.upper())

    for purchase_balance_item in purchase_balance.stocks_balance:
        table_detail.add_row(
            purchase_balance_item.unit.ticker,
            f"{purchase_balance_item.unit.price:.2f}",
            str(purchase_balance_item.count),
            f"{purchase_balance_item.total_amount:.2f}",
            purchase_balance_item.unit.updated_at.astimezone(
                ZoneInfo(get_config().timezone_local)
            ).isoformat()[:19],
        )

    table_resume = Table(box=None)
    for key in ("total", "value"):
        if key in ("value",):
            table_resume.add_column(key.upper(), justify="right")
        else:
            table_resume.add_column(key.upper())
    table_resume.add_row(
        "SHARE QUANTITY",
        f"{purchase_balance.stock_count}",
    )
    table_resume.add_row(
        "SPENT AMOUNT",
        f"{purchase_balance.amount_spent:.2f}",
    )
    table_resume.add_row(
        "REMAINING AMOUNT",
        f"{purchase_balance.remaining_balance:.2f}",
    )

    console.print(table_detail)
    console.print("")
    console.print(table_resume)


@app.command("reit", help="Reit purchase balancing.")
def reit_purchase_balancing(
    tickers: Annotated[
        list[str],
        Argument(help="Reit tickers.", autocompletion=complete_reit_tickers),
    ],
    amount: Annotated[float, Option(help="Amount invested.")],
):
    purchase_balance: PurchaseBalance = aio.run(
        purchase_balance_service.reit_purchase_balancing(
            tickers=tickers, amount_invested=Decimal(str(amount))
        )
    )
    table_detail = Table(box=None)
    for key in ("ticket", "price", "count", "total", "updated_at"):
        if key in ("price", "total", "count"):
            table_detail.add_column(key.upper(), justify="right")
        else:
            table_detail.add_column(key.upper())

    for purchase_balance_item in purchase_balance.stocks_balance:
        table_detail.add_row(
            purchase_balance_item.unit.ticker,
            f"{purchase_balance_item.unit.price:.2f}",
            str(purchase_balance_item.count),
            f"{purchase_balance_item.total_amount:.2f}",
            purchase_balance_item.unit.updated_at.astimezone(
                ZoneInfo(get_config().timezone_local)
            ).isoformat()[:19],
        )

    table_resume = Table(box=None)
    for key in ("total", "value"):
        if key in ("value",):
            table_resume.add_column(key.upper(), justify="right")
        else:
            table_resume.add_column(key.upper())
    table_resume.add_row(
        "SHARE QUANTITY",
        f"{purchase_balance.stock_count}",
    )
    table_resume.add_row(
        "SPENT AMOUNT",
        f"{purchase_balance.amount_spent:.2f}",
    )
    table_resume.add_row(
        "REMAINING AMOUNT",
        f"{purchase_balance.remaining_balance:.2f}",
    )

    console.print(table_detail)
    console.print("")
    console.print(table_resume)
