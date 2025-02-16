from typing import Protocol, Self, TypeVar

from httpx import AsyncClient

T = TypeVar("T")


class ScrapingInterface(Protocol[T]):
    def __init__(self: Self, client: AsyncClient): ...

    async def get_by_ticker(self: Self, ticker: str) -> T: ...

    async def list_by_tickers(self: Self, tickers: list[str]) -> list[T]: ...

    async def list_tickers_most_popular(self: Self) -> list[str]: ...
