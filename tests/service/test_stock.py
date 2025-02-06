import pytest

from app.resource.stock import Stock
from app.service import stock as stock_service


@pytest.mark.asyncio
async def test_get_stock_ok_01():
    ticker = "PETR3"
    stock = await stock_service.get_stock(ticker=ticker)
    assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_ok_01():
    tickers = ["B3SA3", "AMER3"]
    stocks = await stock_service.list_stocks(tickers=tickers)
    for stock in stocks:
        assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_most_popular_ok_01():
    stocks = await stock_service.list_stocks_most_popular()
    for stock in stocks:
        assert isinstance(stock, Stock)
