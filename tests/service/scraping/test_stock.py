import pytest

from app.resource.stock import Stock
from app.service.scraping import stock as stock_scraping


@pytest.mark.asyncio
async def test_get_stock_ok_01():
    ticker = "bbas3"
    stock = await stock_scraping.get_stock(ticker=ticker)
    assert isinstance(stock, Stock)


@pytest.mark.asyncio
async def test_list_stocks_ok_01():
    tickers = ["bbas3", "vale3"]
    stocks = await stock_scraping.list_stocks(tickers=tickers)
    for stock in stocks:
        assert isinstance(stock, Stock)
