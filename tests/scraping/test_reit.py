import pytest

from app.resource.reit import Reit
from app.scraping import reit as reit_scraping


@pytest.mark.asyncio
async def test_get_reit_ok_01():
    ticker = "BPML11"
    reit = await reit_scraping.get_reit(ticker=ticker)
    assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_ok_01():
    tickers = ["HTMX11", "PORD11"]
    reits = await reit_scraping.list_reits(tickers=tickers)
    for reit in reits:
        assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_most_popular_ok_01():
    reits = await reit_scraping.list_reits_most_popular()
    for reit in reits:
        assert isinstance(reit, Reit)
