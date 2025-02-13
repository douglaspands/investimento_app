import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from typing import Self

from httpx import AsyncClient, HTTPStatusError, RequestError
from parsel import Selector
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.config import get_config
from app.resource.reit import Reit
from app.scraping.interface import ScrapingInterface


class StatusInvestReitScraping(ScrapingInterface[Reit]):
    """StatusInvest Reit Scraping."""

    def __init__(self: Self, client: AsyncClient):
        """Constructor.

        Args:
            client (AsyncClient): HttpClient.
        """
        self._client = client
        self._url = "https://statusinvest.com.br"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache",
        }

    @retry(
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def get_by_ticker(
        self: Self,
        ticker: str,
    ) -> Reit:
        """Get REIT information from StatusInvest.

        Args:
            ticker (str): Reit ticker.
            client (AsyncClient): Async HTTPX client.

        Returns:
            Reit: REIT information.
        """
        config = get_config()
        ticker = ticker.strip()
        response = await self._client.get(
            f"{self._url}/fundos-imobiliarios/{ticker.lower()}",
            headers=self._headers,
            timeout=config.scraping_timeout_ttl,
        )
        response.raise_for_status()
        selector = Selector(text=response.text)
        for result in selector.xpath("//h1[@class='lh-4']/small/text()"):
            name = str(result).strip()
            break
        for result in selector.xpath(
            "//*[@id='fund-section']/div/div/div[2]/div/div[6]/div/div/strong/text()"
        ):
            segment = str(result).strip()
            break
        for result in selector.xpath(
            '//div[@title="Valor atual do ativo"]/strong/text()'
        ):
            price = Decimal(str(result).strip().replace(",", "."))
            break
        for result in selector.xpath(
            "//*[@id='fund-section']/div/div/div[3]/div/div[2]/div[1]/div/strong/text()"
        ):
            admin = str(result).strip()
            break
        return Reit(
            name=name,
            ticker=ticker.upper(),
            price=price,
            segment=segment,
            admin=admin,
            origin="StatusInvest",
            updated_at=datetime.now(tz=timezone.utc),
        )

    @retry(
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def list_tickers_most_popular(
        self: Self,
    ) -> list[str]:
        """List the most popular tickers (about REITs) from StatusInvest.

        Args:
            client (AsyncClient): Async HTTPX client.

        Returns:
            list[str]: List of most popular tickers.
        """
        config = get_config()
        response = await self._client.get(
            f"{self._url}/fundos-imobiliarios",
            headers=self._headers,
            timeout=config.scraping_timeout_ttl,
        )
        response.raise_for_status()
        selector = Selector(text=response.text)
        tickers = []
        for result in selector.xpath(
            '//*[@id="main-2"]/section[2]/div/div[1]/div[2]/table/tr/td/a/div[2]/h4'
        ):
            tickers.append(str(result.css("strong::text").pop()).strip())
        return tickers

    async def list_by_tickers(
        self: Self,
        tickers: list[str],
    ) -> list[Reit]:
        """
        List REITs information from StatusInvest.

        Args:
            tickers (list[str]): List of Reit tickers.
            client (AsyncClient): Async HTTPX client.

        Returns:
            list[Stock]: List of REIT datas.
        """
        return await asyncio.gather(
            *[self.get_by_ticker(ticker=ticker) for ticker in tickers]
        )
