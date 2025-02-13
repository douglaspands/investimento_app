from typing import Protocol, Self, TypeVar

from httpx import AsyncClient

T = TypeVar("T")


class ScrapingInterface(Protocol[T]):
    def __init__(self: Self, client: AsyncClient):
        pass

    async def get_by_ticker(self: Self, ticker: str) -> T:
        pass

    async def list_by_tickers(self: Self, tickers: list[str]) -> list[T]:
        pass

    async def list_tickers_most_popular(self: Self) -> list[str]:
        pass
