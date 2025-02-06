import pytest

from app.resource.stock import Stock
from app.scraping import stock as stock_scraping


@pytest.mark.asyncio
async def test_get_stock_ok_01():
    ticker = "PETR3"
    stock = await stock_scraping.get_stock(ticker=ticker)
    assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_ok_01():
    tickers = ["B3SA3", "AMER3"]
    stocks = await stock_scraping.list_stocks(tickers=tickers)
    for stock in stocks:
        assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_most_popular_ok_01():
    stocks = await stock_scraping.list_stocks_most_popular()
    for stock in stocks:
        assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_most_popular_tickers_ok_01():
    tickers = await stock_scraping.list_tickers_most_popular()
    for ticker in tickers:
        assert isinstance(ticker, str)
