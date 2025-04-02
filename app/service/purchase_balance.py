from datetime import datetime
from decimal import Decimal

from app.enum.scraping import ReitScrapingOriginEnum, StockScrapingOriginEnum
from app.resource.purchase_balance import PurchaseBalance, StockBalance
from app.resource.reit import Reit
from app.resource.stock import Stock
from app.service import reit as reit_service
from app.service import stock as stock_service


async def stock_purchase_balancing(
    amount_invested: Decimal, tickers: list[str]
) -> PurchaseBalance:
    """Stock purchase balancing.

    Args:
        amount_invested (Decimal): Amount invested.
        tickers (list[str]): List of stock tickers.

    Returns:
        PurchaseBalance: Purchase balance.
    """
    stocks = await stock_service.list_stocks(
        tickers=tickers, origin=StockScrapingOriginEnum.STATUS_INVEST
    )
    stocks_order: dict[str, Stock] = {}
    tickers_ = tickers.copy()
    tickers_.reverse()
    while tickers_:
        for stock in stocks:
            if tickers_ and stock.ticker == tickers_[-1]:
                stocks_order[tickers_[-1]] = stock
                tickers_.pop()
    return await _purchase_balancing(
        amount_invested=amount_invested, stocks=list(stocks_order.values())
    )


async def reit_purchase_balancing(
    amount_invested: Decimal, tickers: list[str]
) -> PurchaseBalance:
    """Reit purchase balancing.

    Args:
        amount_invested (Decimal): Amount invested.
        tickers (list[str]): List of Reit tickers.

    Returns:
        PurchaseBalance: Purchase balance.
    """
    reits = await reit_service.list_reits(
        tickers=tickers, origin=ReitScrapingOriginEnum.STATUS_INVEST
    )
    reits_order: dict[str, Reit] = {}
    tickers_ = tickers.copy()
    tickers_.reverse()
    while tickers_:
        for reit in reits:
            if tickers_ and reit.ticker == tickers_[-1]:
                reits_order[tickers_[-1]] = reit
                tickers_.pop()
    return await _purchase_balancing(
        amount_invested=amount_invested, stocks=list(reits_order.values())
    )


async def _purchase_balancing(
    amount_invested: Decimal, stocks: list[Stock] | list[Reit]
) -> PurchaseBalance:
    """Purchase balancing.

    Args:
        amount_invested (Decimal): Amount invested.
        stocks (list[Stock] | list[Reit]): List of stocks or reits for invested.

    Returns:
        PurchaseBalance: Result of purchasing.
    """
    stock_count = len(stocks)
    stock_value = amount_invested / stock_count
    purchased_stocks: list[StockBalance] = []
    remaining_balance = amount_invested
    price_min = Decimal("Infinity")

    for stock in stocks:
        price_min = stock.price if stock.price < price_min else price_min
        count = int(stock_value / stock.price)
        purchase_balance = StockBalance(
            unit=stock,
            count=count,
        )
        purchased_stocks.append(purchase_balance)
        remaining_balance -= purchase_balance.total_amount

    while remaining_balance >= price_min:
        for i in range(stock_count):
            if remaining_balance >= purchased_stocks[i].unit.price:
                purchased_stocks[i].count += 1
                remaining_balance -= purchased_stocks[i].unit.price

    return PurchaseBalance(
        stocks_balance=purchased_stocks,
        amount_invested=amount_invested,
        created_at=datetime.now(),
    )
