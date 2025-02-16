from httpx import AsyncClient

from app.enum.scraping import StockScrapingOriginEnum
from app.resource.stock import Stock
from app.scraping.interface import ScrapingInterface
from app.scraping.status_invest.stock import StatusInvestStockScraping


def stock_scraping_factory(
    origin: StockScrapingOriginEnum, client: AsyncClient
) -> ScrapingInterface[Stock]:
    """Factory function to create a scraping interface for stock.
    Args:
        origin (StockScrapingOriginEnum): The origin of the Stock data to scrape.
        client (AsyncClient): The httpx AsyncClient to use for making requests.
    Returns:
        ScrapingInterface[Stock]: A scraping interface for stock.
    """
    match origin:
        case StockScrapingOriginEnum.STATUS_INVEST:
            return StatusInvestStockScraping(client=client)
        case _:
            raise ValueError("origin not found")
