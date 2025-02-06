from app.resource.reit import Reit
from app.scraping import reit as reit_scraping


async def get_reit(ticker: str) -> Reit:
    """Get REIT information.

    Args:
        ticker (str): Reit ticker.

    Returns:
        Reit: REIT information.
    """
    return await reit_scraping.get_reit(ticker=ticker)


async def list_reits(tickers: list[str]) -> list[Reit]:
    """
    List REITs information.

    Args:
        tickers (list[str]): List of Reit tickers.

    Returns:
        list[Stock]: List of REIT datas.
    """
    return await reit_scraping.list_reits(tickers=tickers)


async def list_reits_most_popular() -> list[Reit]:
    """
    Get most popular REITs information.

    Returns:
        list[Reit]: List of Reit datas.
    """
    return await reit_scraping.list_reits_most_popular()
