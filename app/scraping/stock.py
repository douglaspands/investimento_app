from httpx import AsyncClient

from app.enum.scraping import StockScrapingOriginEnum
from app.resource.stock import Stock
from app.scraping.interface import ScrapingInterface
from app.scraping.status_invest.stock import StatusInvestStockScraping


def stock_scraping_factory(
    origin: StockScrapingOriginEnum, client: AsyncClient
) -> ScrapingInterface[Stock]:
    match origin:
        case StockScrapingOriginEnum.STATUS_INVEST:
            return StatusInvestStockScraping(client=client)
        case _:
            raise ValueError("origin not found")
