import asyncio
from datetime import datetime, timezone
from decimal import Decimal

from httpx import AsyncClient, HTTPStatusError, RequestError
from parsel import Selector
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.config import get_config
from app.resource.stock import Stock

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}
scraping_url = "https://statusinvest.com.br/acoes"


@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((RequestError, HTTPStatusError)),
)
async def get_stock(client: AsyncClient, ticker: str) -> Stock:
    """Get stock information from StatusInvest.

    Args:
        ticker (str): Stock ticker.
        client (AsyncClient): Async HTTPX client.

    Returns:
        Stock: Stock information.
    """
    config = get_config()
    ticker = ticker.strip()
    response = await client.get(
        f"{scraping_url}/{ticker.lower()}",
        headers=headers,
        timeout=config.scraping_timeout_ttl,
    )
    response.raise_for_status()
    selector = Selector(text=response.text)
    for result in selector.xpath("//h1[@title]"):
        name = result.attrib["title"].split("-").pop().strip()
        break
    for result in selector.xpath('//div[@title="Valor atual do ativo"]/strong/text()'):
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
        updated_at=datetime.now(tz=timezone.utc),
    )


@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((RequestError, HTTPStatusError)),
)
async def list_tickers_most_popular(client: AsyncClient) -> list[str]:
    """List the most popular tickers (About stocks) from StatusInvest.

    Args:
        client (AsyncClient): Async HTTPX client.

    Returns:
        list[str]: List of most popular tickers.
    """
    config = get_config()
    response = await client.get(
        scraping_url,
        headers=headers,
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


async def list_stocks(client: AsyncClient, tickers: list[str]) -> list[Stock]:
    """
    List stocks information from StatusInvest.

    Args:
        tickers (list[str]): List of stock tickers.
        client (AsyncClient): Async HTTPX client.

    Returns:
        list[Stock]: List of Stock datas.
    """
    return await asyncio.gather(
        *[get_stock(ticker=ticker, client=client) for ticker in tickers]
    )
