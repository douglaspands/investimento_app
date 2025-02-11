from datetime import datetime, timedelta

from app.common.database import db_session_maker
from app.common.http import get_httpclient
from app.config import get_config
from app.model.reit import Reit as ReitModel
from app.repository import reit as reit_repository
from app.resource.reit import Reit
from app.scraping import reit as reit_scraping

SessionLocal = db_session_maker()


async def get_reit(ticker: str) -> Reit:
    """Get reit information.

    Args:
        ticker (str): Reit ticker.

    Returns:
        Reit: Reit information.
    """
    config = get_config()
    async with SessionLocal() as db_session:
        async with get_httpclient() as http_client:
            reit = await reit_repository.get_by_ticker(
                session=db_session, ticker=ticker
            )
            if reit:
                if reit.updated_at and reit.updated_at < (
                    datetime.now() - timedelta(seconds=config.reit_cache_ttl)
                ):
                    stoke_now = await reit_scraping.get_reit(
                        ticker=ticker, client=http_client
                    )
                    reit.price = stoke_now.price
                    reit.updated_at = stoke_now.updated_at
                    await reit_repository.update_by_ticker(
                        session=db_session,
                        ticker=ticker,
                        price=stoke_now.price,
                        updated_at=stoke_now.updated_at,
                    )
            else:
                stoke_now = await reit_scraping.get_reit(
                    ticker=ticker, client=http_client
                )
                reit = await reit_repository.create(
                    session=db_session, reit=ReitModel(**stoke_now.__dict__)
                )
    return Reit(**reit.__dict__)


async def list_reits(tickers: list[str]) -> list[Reit]:
    """
    List reits information.

    Args:
        tickers (list[str]): List of reit tickers.

    Returns:
        list[Reit]: List of Reit datas.
    """
    config = get_config()
    result: list[Reit] = []
    async with SessionLocal() as db_session, db_session.begin():
        async with get_httpclient() as http_client:
            updated_at = datetime.now() - timedelta(seconds=config.reit_cache_ttl)
            reits = await reit_repository.get_all_by_tickers(
                session=db_session, tickers=tickers, updated_at=updated_at
            )
            diff = set(tickers) - set([s.ticker for s in reits])
            if diff:
                new_reits = await reit_scraping.list_reits(
                    client=http_client, tickers=list(diff)
                )
                for nr in new_reits:
                    reit = await reit_repository.get_by_ticker(
                        session=db_session, ticker=nr.ticker
                    )
                    if reit:
                        await reit_repository.update_by_ticker(
                            session=db_session,
                            ticker=nr.ticker,
                            price=nr.price,
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


async def list_reits_most_popular() -> list[Reit]:
    """
    Get most popular reits information.

    Returns:
        list[Reit]: List of Reit datas.
    """
    config = get_config()
    result: list[Reit] = []
    async with SessionLocal() as db_session, db_session.begin():
        async with get_httpclient() as http_client:
            tickers = await reit_scraping.list_tickers_most_popular(client=http_client)
            updated_at = datetime.now() - timedelta(seconds=config.reit_cache_ttl)
            reits = await reit_repository.get_all_by_tickers(
                session=db_session, tickers=tickers, updated_at=updated_at
            )
            diff = set(tickers) - set([s.ticker for s in reits])
            if diff:
                new_reits = await reit_scraping.list_reits(
                    client=http_client, tickers=list(diff)
                )
                for nr in new_reits:
                    reit = await reit_repository.get_by_ticker(
                        session=db_session, ticker=nr.ticker
                    )
                    if reit:
                        await reit_repository.update_by_ticker(
                            session=db_session,
                            ticker=nr.ticker,
                            price=nr.price,
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
