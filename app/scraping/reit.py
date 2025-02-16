from httpx import AsyncClient

from app.enum.scraping import ReitScrapingOriginEnum
from app.resource.reit import Reit
from app.scraping.interface import ScrapingInterface
from app.scraping.status_invest.reit import StatusInvestReitScraping


def reit_scraping_factory(
    origin: ReitScrapingOriginEnum, client: AsyncClient
) -> ScrapingInterface[Reit]:
    """Factory function to create a scraping interface for a REIT.
    Args:
        origin (ReitScrapingOriginEnum): The origin of the REIT data to scrape.
        client (AsyncClient): The httpx AsyncClient to use for making requests.
    Returns:
        ScrapingInterface[Reit]: A scraping interface for the reit.
    """
    match origin:
        case ReitScrapingOriginEnum.STATUS_INVEST:
            return StatusInvestReitScraping(client=client)
        case _:
            raise ValueError("origin not found")
