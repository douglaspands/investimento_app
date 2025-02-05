import asyncio
from datetime import datetime
from decimal import Decimal

from httpx import AsyncClient
from parsel import Selector

from app.resource.reit import Reit

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


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
            f"https://statusinvest.com.br/fundos-imobiliarios/{ticker.lower()}",
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
