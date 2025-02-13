import pytest

from app.common.http import get_httpclient
from app.resource.reit import Reit
from app.scraping import reit as reit_scraping


@pytest.mark.asyncio
async def test_get_reit_ok_01():
    ticker = "BPML11"
    async with get_httpclient() as client:
        reit = await reit_scraping.get_reit(ticker=ticker, client=client)
    assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_ok_01():
    tickers = ["HTMX11", "PORD11"]
    async with get_httpclient() as client:
        reits = await reit_scraping.list_reits(tickers=tickers, client=client)
    for reit in reits:
        assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_most_popular_tickets_ok_01():
    async with get_httpclient() as client:
        tickers = await reit_scraping.list_tickers_most_popular(client=client)
    for ticker in tickers:
        assert isinstance(ticker, str)
