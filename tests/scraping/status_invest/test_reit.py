import pytest

from app.common.http import get_httpclient
from app.resource.reit import Reit
from app.scraping.status_invest.reit import StatusInvestReitScraping


@pytest.mark.asyncio
async def test_get_reit_ok_01():
    ticker = "BPML11"
    async with get_httpclient() as client:
        reit_scraping = StatusInvestReitScraping(client=client)
        reit = await reit_scraping.get_by_ticker(ticker=ticker)
    assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_ok_01():
    tickers = ["HTMX11", "PORD11"]
    async with get_httpclient() as client:
        reit_scraping = StatusInvestReitScraping(client=client)
        reits = await reit_scraping.list_by_tickers(tickers=tickers)
    for reit in reits:
        assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_most_popular_tickets_ok_01():
    async with get_httpclient() as client:
        reit_scraping = StatusInvestReitScraping(client=client)
        tickers = await reit_scraping.list_tickers_most_popular()
    for ticker in tickers:
        assert isinstance(ticker, str)
