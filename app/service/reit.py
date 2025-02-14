from datetime import datetime, timedelta

from app.common.db import session_maker
from app.common.http import get_client
from app.config import get_config
from app.enum.scraping import ScrapingOriginEnum
from app.model.reit import Reit as ReitModel
from app.repository import reit as reit_repository
from app.resource.reit import Reit
from app.scraping.reit import reit_scraping_factory

SessionLocal = session_maker()


async def get_reit(ticker: str, origin: ScrapingOriginEnum) -> Reit:
    """Get reit information.

    Args:
        ticker (str): Reit ticker.
        origin (ScrapingOriginEnum): Scraping origin.

    Returns:
        Reit: Reit information.
    """
    config = get_config()
    async with SessionLocal() as db_session:
        reit = await reit_repository.get_by_ticker(session=db_session, ticker=ticker)
        if reit:
            if reit.updated_at and reit.updated_at < (
                datetime.now() - timedelta(seconds=config.reit_cache_ttl)
            ):
                async with get_client() as http_client:
                    reit_scraping = reit_scraping_factory(
                        origin=origin, client=http_client
                    )
                    nr = await reit_scraping.get_by_ticker(ticker=ticker)
                    reit = await reit_repository.update_by_ticker(
                        session=db_session,
                        ticker=nr.ticker,
                        name=nr.name,
                        price=nr.price,
                        segment=nr.segment,
                        admin=nr.admin,
                        origin=nr.origin,
                        updated_at=nr.updated_at,
                    )
        else:
            async with get_client() as http_client:
                reit_scraping = reit_scraping_factory(origin=origin, client=http_client)
                nr = await reit_scraping.get_by_ticker(ticker=ticker)
                reit = await reit_repository.create(
                    session=db_session, reit=ReitModel(**nr.__dict__)
                )
    return Reit(**reit.__dict__)


async def list_reits(tickers: list[str], origin: ScrapingOriginEnum) -> list[Reit]:
    """
    List reits information.

    Args:
        tickers (list[str]): List of reit tickers.
        origin (ScrapingOriginEnum): Scraping origin.

    Returns:
        list[Reit]: List of Reit datas.
    """
    config = get_config()
    result: list[Reit] = []
    async with SessionLocal() as db_session, db_session.begin():
        async with get_client() as http_client:
            updated_at = datetime.now() - timedelta(seconds=config.reit_cache_ttl)
            reits = await reit_repository.get_all_by_tickers(
                session=db_session, tickers=tickers, updated_at=updated_at
            )
            diff = set(tickers) - set([s.ticker for s in reits])
            if diff:
                async with get_client() as http_client:
                    reit_scraping = reit_scraping_factory(
                        origin=origin, client=http_client
                    )
                    new_reits = await reit_scraping.list_by_tickers(tickers=list(diff))
                    for nr in new_reits:
                        reit = await reit_repository.get_by_ticker(
                            session=db_session, ticker=nr.ticker
                        )
                        if reit:
                            await reit_repository.update_by_ticker(
                                session=db_session,
                                ticker=nr.ticker,
                                name=nr.name,
                                price=nr.price,
                                segment=nr.segment,
                                admin=nr.admin,
                                origin=nr.origin,
                                updated_at=nr.updated_at,
                            )
                        else:
                            await reit_repository.create(
                                session=db_session, reit=ReitModel(**nr.__dict__)
                            )
                    result = [Reit(**s.__dict__) for s in reits] + new_reits
            else:
                result = [Reit(**s.__dict__) for s in reits]
    return result


async def list_reits_most_popular(origin: ScrapingOriginEnum) -> list[Reit]:
    """
    Get most popular reits information.

    Args:
        origin (ScrapingOriginEnum): Scraping origin.

    Returns:
        list[Reit]: List of Reit datas.
    """
    config = get_config()
    result: list[Reit] = []
    async with SessionLocal() as db_session, db_session.begin():
        async with get_client() as http_client:
            reit_scraping = reit_scraping_factory(origin=origin, client=http_client)
            tickers = await reit_scraping.list_tickers_most_popular()
            updated_at = datetime.now() - timedelta(seconds=config.reit_cache_ttl)
            reits = await reit_repository.get_all_by_tickers(
                session=db_session, tickers=tickers, updated_at=updated_at
            )
            diff = set(tickers) - set([s.ticker for s in reits])
            if diff:
                new_reits = await reit_scraping.list_by_tickers(tickers=list(diff))
                for nr in new_reits:
                    reit = await reit_repository.get_by_ticker(
                        session=db_session, ticker=nr.ticker
                    )
                    if reit:
                        await reit_repository.update_by_ticker(
                            session=db_session,
                            ticker=nr.ticker,
                            name=nr.name,
                            price=nr.price,
                            segment=nr.segment,
                            admin=nr.admin,
                            origin=nr.origin,
                            updated_at=nr.updated_at,
                        )
                    else:
                        await reit_repository.create(
                            session=db_session, reit=ReitModel(**nr.__dict__)
                        )
                result = [Reit(**s.__dict__) for s in reits] + new_reits
            else:
                result = [Reit(**s.__dict__) for s in reits]
    return result
