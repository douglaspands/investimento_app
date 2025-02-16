from typing import Iterable, Self

from httpx import AsyncClient, HTTPStatusError, RequestError
from parsel import Selector
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.common.http import get_headers
from app.config import get_config
from app.resource.ticker import Ticker, TickerTypeEnum


class FiiReitScraping:
    """fii.com.br Reit Scraping."""

    def __init__(self: Self, client: AsyncClient):
        """Constructor.

        Args:
            client (AsyncClient): HttpClient.
        """
        self._client = client
        self._url = "https://fiis.com.br"

    @retry(
        wait=wait_fixed(5),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def list_tickers(self: Self) -> Iterable[Ticker]:
        tickers = []
        config = get_config()
        response = await self._client.get(
            f"{self._url}/lista-de-fundos-imobiliarios/",
            headers=get_headers(),
            timeout=config.scraping_timeout_ttl,
        )
        response.raise_for_status()
        selector = Selector(text=response.text)
        for tag in selector.xpath('//*[contains(@id, "letter-id-")]/div/div'):
            card = Selector(text=tag.extract())
            reit = {"help": ""}
            for symbol in card.xpath('//div/a/div[@class="tickerBox__title"]//text()'):
                if s := str(symbol).strip():
                    reit["symbol"] = s
                    break
            for help in card.xpath('//div/div[@class="tickerBox__desc"]//text()'):
                reit["help"] = str(help).strip()
                break
            if reit.get("symbol"):
                tickers.append(
                    Ticker(
                        symbol=reit["symbol"],
                        help=reit["help"],
                        type=TickerTypeEnum.REIT,
                    )
                )
        return tickers
