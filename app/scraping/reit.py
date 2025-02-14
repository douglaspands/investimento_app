from httpx import AsyncClient

from app.enum.scraping import ScrapingOriginEnum
from app.resource.reit import Reit
from app.scraping.interface import ScrapingInterface
from app.scraping.status_invest.reit import StatusInvestReitScraping


def reit_scraping_factory(
    origin: ScrapingOriginEnum, client: AsyncClient
) -> ScrapingInterface[Reit]:
    match origin:
        case ScrapingOriginEnum.STATUS_INVEST:
            return StatusInvestReitScraping(client=client)
        case _:
            raise ValueError("origin not found")
