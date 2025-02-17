from typing import Iterable, Self

from httpx import AsyncClient, HTTPStatusError, RequestError
from parsel import Selector
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.common.http import get_headers
from app.config import get_config
from app.resource.ticker import Ticker, TickerTypeEnum


class DadosDeMercadoStockScraping:
    """Dados De Mercado Stock Scraping."""

    def __init__(self: Self, client: AsyncClient):
        """Constructor.

        Args:
            client (AsyncClient): HttpClient.
        """
        self._client = client
        self._url = "https://www.dadosdemercado.com.br"

    @retry(
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def list_tickers(self: Self) -> Iterable[Ticker]:
        config = get_config()
        response = await self._client.get(
            f"{self._url}/acoes",
            headers=get_headers(),
            timeout=config.scraping_timeout_ttl,
        )
        response.raise_for_status()
        selector = Selector(text=response.text)
        tickers = []
        helpers = []
        ignored = {}
        for row in selector.xpath('//*[@id="stocks"]/tbody/tr'):
            for idx, column in enumerate(row.xpath("//td[1]//text()")):
                ticker = str(column).strip()
                if ticker in tickers:
                    ignored[idx] = True
                    continue
                tickers.append(ticker)
            for idx, column in enumerate(row.xpath("//td[2]//text()")):
                if ignored.get(idx):
                    continue
                helpers.append(str(column).strip())
            break
        return [
            Ticker(symbol=t[0], help=t[1], type=TickerTypeEnum.STOCK)
            for t in list(zip(tickers, helpers))
        ]
