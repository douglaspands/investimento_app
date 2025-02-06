import pytest

from app.resource.reit import Reit
from app.service import reit as reit_service


@pytest.mark.asyncio
async def test_get_reit_ok_01():
    ticker = "BPML11"
    reit = await reit_service.get_reit(ticker=ticker)
    assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_ok_01():
    tickers = ["HTMX11", "PORD11"]
    reits = await reit_service.list_reits(tickers=tickers)
    for reit in reits:
        assert isinstance(reit, Reit)


@pytest.mark.asyncio
async def test_list_reits_most_popular_ok_01():
    reits = await reit_service.list_reits_most_popular()
    for reit in reits:
        assert isinstance(reit, Reit)
