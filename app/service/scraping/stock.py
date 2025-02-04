import asyncio
from datetime import datetime
from decimal import Decimal

from httpx import AsyncClient
from parsel import Selector

from app.resource.stock import Stock

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


async def get_stock(ticker: str, client: AsyncClient | None = None) -> Stock:
    """Get stock information from StatusInvest.

    Args:
        ticker (str): Stock ticker.

    Returns:
        Stock: Stock information.
    """
    ticker = ticker.strip()
    _client = client if client else AsyncClient()
    try:
        response = await _client.get(
            f"https://statusinvest.com.br/acoes/{ticker.lower()}", headers=headers
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
        description = "\n".join(
            [str(p).strip() for p in selector.xpath("//div/p[not(@*)]/text()")]
        )
        return Stock(
            name=name,
            ticker=ticker.upper(),
            price=price,
            description=description,
            updated_at=datetime.now(),
        )
    finally:
        if not client:
            await _client.aclose()


async def list_stocks(tickers: list[str]) -> list[Stock]:
    """
    List stocks information.

    Args:
        tickers (list[str]): List of stock tickers.

    Returns:
        list[Stock]: List of Stock datas.
    """
    async with AsyncClient() as client:
        return await asyncio.gather(
            *[get_stock(ticker=ticker, client=client) for ticker in tickers]
        )
