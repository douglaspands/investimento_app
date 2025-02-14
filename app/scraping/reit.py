from httpx import AsyncClient

from app.enum.scraping import ReitScrapingOriginEnum
from app.resource.reit import Reit
from app.scraping.interface import ScrapingInterface
from app.scraping.status_invest.reit import StatusInvestReitScraping


def reit_scraping_factory(
    origin: ReitScrapingOriginEnum, client: AsyncClient
) -> ScrapingInterface[Reit]:
    match origin:
        case ReitScrapingOriginEnum.STATUS_INVEST:
            return StatusInvestReitScraping(client=client)
        case _:
            raise ValueError("origin not found")
