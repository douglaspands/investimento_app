from datetime import datetime, timedelta

from app.common.database import db_session_maker
from app.common.http import get_httpclient
from app.config import get_config
from app.enum.scraping import ScrapingOriginEnum
from app.model.stock import Stock as StockModel
from app.repository import stock as stock_repository
from app.resource.stock import Stock
from app.scraping.stock import stock_scraping_factory

SessionLocal = db_session_maker()


async def get_stock(ticker: str, origin: ScrapingOriginEnum) -> Stock:
    """Get stock information.

    Args:
        ticker (str): Stock ticker.
        origin (ScrapingOriginEnum): Scraping origin.

    Returns:
        Stock: Stock information.
    """
    config = get_config()
    async with SessionLocal() as db_session:
        stock = await stock_repository.get_by_ticker(session=db_session, ticker=ticker)
        if stock:
            if stock.updated_at and stock.updated_at < (
                datetime.now() - timedelta(seconds=config.stock_cache_ttl)
            ):
                async with get_httpclient() as http_client:
                    stock_scraping = stock_scraping_factory(
                        origin=origin, client=http_client
                    )
                    stoke_now = await stock_scraping.get_by_ticker(ticker=ticker)
                    stock.price = stoke_now.price
                    stock.updated_at = stoke_now.updated_at
                    await stock_repository.update_by_ticker(
                        session=db_session,
                        ticker=ticker,
                        price=stoke_now.price,
                        updated_at=stoke_now.updated_at,
                    )
        else:
            async with get_httpclient() as http_client:
                stock_scraping = stock_scraping_factory(
                    origin=origin, client=http_client
                )
                stoke_now = await stock_scraping.get_by_ticker(ticker=ticker)
                stock = await stock_repository.create(
                    session=db_session, stock=StockModel(**stoke_now.__dict__)
                )
    return Stock(**stock.__dict__)


async def list_stocks(tickers: list[str], origin: ScrapingOriginEnum) -> list[Stock]:
    """
    List stocks information.

    Args:
        tickers (list[str]): List of stock tickers.
        origin (ScrapingOriginEnum): Scraping origin.

    Returns:
        list[Stock]: List of Stock datas.
    """
    config = get_config()
    result: list[Stock] = []
    async with SessionLocal() as db_session, db_session.begin():
        updated_at = datetime.now() - timedelta(seconds=config.stock_cache_ttl)
        stocks = await stock_repository.get_all_by_tickers(
            session=db_session, tickers=tickers, updated_at=updated_at
        )
        diff = set(tickers) - set([s.ticker for s in stocks])
        if diff:
            async with get_httpclient() as http_client:
                stock_scraping = stock_scraping_factory(
                    origin=origin, client=http_client
                )
                new_stocks = await stock_scraping.list_by_tickers(tickers=list(diff))
                for ns in new_stocks:
                    stock = await stock_repository.get_by_ticker(
                        session=db_session, ticker=ns.ticker
                    )
                    if stock:
                        await stock_repository.update_by_ticker(
                            session=db_session,
                            ticker=ns.ticker,
                            price=ns.price,
                            updated_at=ns.updated_at,
                        )
                    else:
                        await stock_repository.create(
                            session=db_session, stock=StockModel(**ns.__dict__)
                        )
            result = [Stock(**s.__dict__) for s in stocks] + new_stocks
        else:
            result = [Stock(**s.__dict__) for s in stocks]
    return result


async def list_stocks_most_popular(origin: ScrapingOriginEnum) -> list[Stock]:
    """
    Get most popular stocks information.

    Args:
        origin (ScrapingOriginEnum): Scraping origin.

    Returns:
        list[Stock]: List of Stock datas.
    """
    config = get_config()
    result: list[Stock] = []
    async with SessionLocal() as db_session, db_session.begin():
        async with get_httpclient() as http_client:
            stock_scraping = stock_scraping_factory(origin=origin, client=http_client)
            tickers = await stock_scraping.list_tickers_most_popular()
            updated_at = datetime.now() - timedelta(seconds=config.stock_cache_ttl)
            stocks = await stock_repository.get_all_by_tickers(
                session=db_session, tickers=tickers, updated_at=updated_at
            )
            diff = set(tickers) - set([s.ticker for s in stocks])
            if diff:
                new_stocks = await stock_scraping.list_by_tickers(tickers=list(diff))
                for ns in new_stocks:
                    stock = await stock_repository.get_by_ticker(
                        session=db_session, ticker=ns.ticker
                    )
                    if stock:
                        await stock_repository.update_by_ticker(
                            session=db_session,
                            ticker=ns.ticker,
                            price=ns.price,
                            updated_at=ns.updated_at,
                        )
                    else:
                        await stock_repository.create(
                            session=db_session, stock=StockModel(**ns.__dict__)
                        )
                result = [Stock(**s.__dict__) for s in stocks] + new_stocks
            else:
                result = [Stock(**s.__dict__) for s in stocks]
    return result
