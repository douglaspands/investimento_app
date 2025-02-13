import pytest

from app.common.http import get_httpclient
from app.resource.stock import Stock
from app.scraping.status_invest import stock as stock_scraping


@pytest.mark.asyncio
async def test_get_stock_ok_01():
    ticker = "PETR3"
    async with get_httpclient() as client:
        stock = await stock_scraping.get_stock(ticker=ticker, client=client)
    assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_ok_01():
    tickers = ["B3SA3", "AMER3"]
    async with get_httpclient() as client:
        stocks = await stock_scraping.list_stocks(tickers=tickers, client=client)
    for stock in stocks:
        assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_most_popular_tickers_ok_01():
    async with get_httpclient() as client:
        tickers = await stock_scraping.list_tickers_most_popular(client=client)
    for ticker in tickers:
        assert isinstance(ticker, str)
