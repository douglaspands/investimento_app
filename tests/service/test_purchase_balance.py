from decimal import Decimal

import pytest

from app.resource.purchase_balance import PurchaseBalance
from app.service.purchase_balance import (
    reit_purchase_balancing,
    stock_purchase_balancing,
)


@pytest.mark.asyncio
async def test_stock_purchase_balancing_ok_01():
    tickers = ["B3SA3", "AMER3"]
    amount_invested = Decimal("500.00")
    result = await stock_purchase_balancing(
        tickers=tickers, amount_invested=amount_invested
    )
    assert isinstance(result, PurchaseBalance)


@pytest.mark.asyncio
async def test_reit_purchase_balancing_ok_01():
    tickers = ["HTMX11", "PORD11"]
    amount_invested = Decimal("500.00")
    result = await reit_purchase_balancing(
        tickers=tickers, amount_invested=amount_invested
    )
    assert isinstance(result, PurchaseBalance)
