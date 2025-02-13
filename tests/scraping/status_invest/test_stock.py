import pytest

from app.common.http import get_httpclient
from app.resource.stock import Stock
from app.scraping.status_invest.stock import StatusInvestStockScraping


@pytest.mark.asyncio
async def test_get_stock_ok_01():
    ticker = "PETR3"
    async with get_httpclient() as client:
        stock_scraping = StatusInvestStockScraping(client=client)
        stock = await stock_scraping.get_by_ticker(ticker=ticker)
    assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_ok_01():
    tickers = ["B3SA3", "AMER3"]
    async with get_httpclient() as client:
        stock_scraping = StatusInvestStockScraping(client=client)
        stocks = await stock_scraping.list_by_tickers(tickers=tickers)
    for stock in stocks:
        assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_most_popular_tickers_ok_01():
    async with get_httpclient() as client:
        stock_scraping = StatusInvestStockScraping(client=client)
        tickers = await stock_scraping.list_tickers_most_popular()
    for ticker in tickers:
        assert isinstance(ticker, str)
