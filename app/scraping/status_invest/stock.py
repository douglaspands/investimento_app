import asyncio
from decimal import Decimal
from typing import Self

from httpx import AsyncClient, HTTPStatusError, RequestError
from parsel import Selector
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.common.http import get_headers
from app.common.utils import now_utc
from app.config import get_config
from app.enum.scraping import ScrapingOriginEnum
from app.resource.stock import Stock
from app.scraping.interface import ScrapingInterface


class StatusInvestStockScraping(ScrapingInterface[Stock]):
    """StatusInvest Stock Scraping."""

    def __init__(self: Self, client: AsyncClient):
        """Constructor.

        Args:
            client (AsyncClient): HttpClient.
        """
        self._client = client
        self._url = "https://statusinvest.com.br"

    @retry(
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def get_by_ticker(self: Self, ticker: str) -> Stock:
        """Get stock information from StatusInvest.

        Args:
            ticker (str): Stock ticker.
            client (AsyncClient): Async HTTPX client.

        Returns:
            Stock: Stock information.
        """
        config = get_config()
        ticker = ticker.strip()
        response = await self._client.get(
            f"{self._url}/acoes/{ticker.lower()}",
            headers=get_headers(),
            timeout=config.scraping_timeout_ttl,
        )
        response.raise_for_status()
        selector = Selector(text=response.text)
        for result in selector.xpath("//h1[@title]"):
            name = result.attrib["title"].split("-").pop().strip()
            break
        for result in selector.xpath(
            '//div[@title="Valor atual do ativo"]/strong/text()'
        ):
            price = Decimal(str(result).strip().replace(",", "."))
            break
        for result in selector.xpath(
            "//*[@id='company-section']/div[1]/div/div[1]/div[2]/h4/small/text()"
        ):
            document = str(result).strip()
            break
        description = "\n".join(
            [str(p).strip() for p in selector.xpath("//div/p[not(@*)]/text()")]
        )
        return Stock(
            name=name,
            ticker=ticker.upper(),
            price=price,
            document=document,
            description=description,
            origin=ScrapingOriginEnum.STATUS_INVEST.value,
            updated_at=now_utc(),
        )

    async def list_by_tickers(self: Self, tickers: list[str]) -> list[Stock]:
        """
        List stocks information from StatusInvest.

        Args:
            tickers (list[str]): List of stock tickers.
            client (AsyncClient): Async HTTPX client.

        Returns:
            list[Stock]: List of Stock datas.
        """
        return await asyncio.gather(
            *[self.get_by_ticker(ticker=ticker) for ticker in tickers]
        )

    @retry(
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def list_tickers_most_popular(self: Self) -> list[str]:
        """List the most popular tickers (About stocks) from StatusInvest.

        Args:
            client (AsyncClient): Async HTTPX client.

        Returns:
            list[str]: List of most popular tickers.
        """
        config = get_config()
        response = await self._client.get(
            f"{self._url}/acoes",
            headers=get_headers(),
            timeout=config.scraping_timeout_ttl,
        )
        response.raise_for_status()
        selector = Selector(text=response.text)
        tickers = []
        for result in selector.xpath(
            '//*[@id="main-2"]/section[3]/div/div[1]/div[2]/table/tr/td/a/div[2]/h4'
        ):
            tickers.append(str(result.css("strong::text").pop()).strip())
        return tickers
