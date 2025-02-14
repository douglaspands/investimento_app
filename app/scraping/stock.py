from httpx import AsyncClient

from app.enum.scraping import ScrapingOriginEnum
from app.resource.stock import Stock
from app.scraping.interface import ScrapingInterface
from app.scraping.status_invest.stock import StatusInvestStockScraping


def stock_scraping_factory(
    origin: ScrapingOriginEnum, client: AsyncClient
) -> ScrapingInterface[Stock]:
    match origin:
        case ScrapingOriginEnum.STATUS_INVEST:
            return StatusInvestStockScraping(client=client)
        case _:
            raise ValueError("origin not found")
