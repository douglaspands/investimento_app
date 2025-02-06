import asyncio
from datetime import datetime
from decimal import Decimal

from httpx import AsyncClient, HTTPStatusError, RequestError
from parsel import Selector
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.resource.reit import Reit

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}
scraping_url = "https://statusinvest.com.br/fundos-imobiliarios"


@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((RequestError, HTTPStatusError)),
)
async def get_reit(ticker: str, client: AsyncClient | None = None) -> Reit:
    """Get REIT information from StatusInvest.

    Args:
        ticker (str): Reit ticker.

    Returns:
        Reit: REIT information.
    """
    ticker = ticker.strip()
    _client = client if client else AsyncClient()
    try:
        response = await _client.get(
            f"{scraping_url}/{ticker.lower()}",
            headers=headers,
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
            updated_at=datetime.now(),
        )
    finally:
        if not client:
            await _client.aclose()


@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((RequestError, HTTPStatusError)),
)
async def list_tickers_most_popular(client: AsyncClient | None = None) -> list[str]:
    """List the most popular tickers (about REITs).

    Args:
        client (AsyncClient | None, optional): Async HTTPX client. Defaults to None.

    Returns:
        list[str]: List of most popular tickers.
    """
    _client = client if client else AsyncClient()
    try:
        response = await _client.get(scraping_url, headers=headers)
        response.raise_for_status()
        selector = Selector(text=response.text)
        tickers = []
        for result in selector.xpath(
            '//*[@id="main-2"]/section[2]/div/div[1]/div[2]/table/tr/td/a/div[2]/h4'
        ):
            tickers.append(str(result.css("strong::text").pop()).strip())
        return tickers
    finally:
        if not client:
            await _client.aclose()


async def list_reits(tickers: list[str]) -> list[Reit]:
    """
    List REITs information.

    Args:
        tickers (list[str]): List of Reit tickers.

    Returns:
        list[Stock]: List of REIT datas.
    """
    async with AsyncClient() as client:
        return await asyncio.gather(
            *[get_reit(ticker=ticker, client=client) for ticker in tickers]
        )


async def list_reits_most_popular() -> list[Reit]:
    """
    Get most popular REITs information.

    Returns:
        list[Reit]: List of Reit datas.
    """
    async with AsyncClient() as client:
        response = await client.get(scraping_url, headers=headers)
        response.raise_for_status()
        selector = Selector(text=response.text)
        tickers = []
        for result in selector.xpath(
            '//*[@id="main-2"]/section[2]/div/div[1]/div[2]/table/tr/td/a/div[2]/h4'
        ):
            tickers.append(str(result.css("strong::text").pop()).strip())
        return await asyncio.gather(
            *[get_reit(ticker=ticker, client=client) for ticker in tickers]
        )
