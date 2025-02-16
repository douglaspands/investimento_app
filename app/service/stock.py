from datetime import datetime, timedelta

from app.common.db import session_maker
from app.common.http import get_client
from app.config import get_config
from app.enum.scraping import StockScrapingOriginEnum
from app.model.stock import Stock as StockModel
from app.repository import stock as stock_repository
from app.resource.stock import Stock
from app.scraping.stock import stock_scraping_factory

SessionLocal = session_maker()


async def get_stock(ticker: str, origin: StockScrapingOriginEnum) -> Stock:
    """Get stock information.

    Args:
        ticker (str): Stock ticker.
        origin (StockScrapingOriginEnum): Scraping origin.

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
                async with get_client() as http_client:
                    stock_scraping = stock_scraping_factory(
                        origin=origin, client=http_client
                    )
                    ns = await stock_scraping.get_by_ticker(ticker=ticker)
                    stock = await stock_repository.update_by_ticker(
                        session=db_session,
                        ticker=ns.ticker,
                        name=ns.name,
                        price=ns.price,
                        document=ns.document,
                        description=ns.description,
                        origin=ns.origin,
                        updated_at=ns.updated_at,
                    )
        else:
            async with get_client() as http_client:
                stock_scraping = stock_scraping_factory(
                    origin=origin, client=http_client
                )
                stoke_now = await stock_scraping.get_by_ticker(ticker=ticker)
                stock = await stock_repository.create(
                    session=db_session, stock=StockModel(**stoke_now.__dict__)
                )
    return Stock(**stock.__dict__)


async def list_stocks(
    tickers: list[str], origin: StockScrapingOriginEnum
) -> list[Stock]:
    """
    List stocks information.

    Args:
        tickers (list[str]): List of stock tickers.
        origin (StockScrapingOriginEnum): Scraping origin.

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
            async with get_client() as http_client:
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
                            name=ns.name,
                            price=ns.price,
                            document=ns.document,
                            description=ns.description,
                            origin=ns.origin,
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


async def list_stocks_most_popular(origin: StockScrapingOriginEnum) -> list[Stock]:
    """
    Get most popular stocks information.

    Args:
        origin (StockScrapingOriginEnum): Scraping origin.

    Returns:
        list[Stock]: List of Stock datas.
    """
    config = get_config()
    result: list[Stock] = []
    async with SessionLocal() as db_session, db_session.begin():
        async with get_client() as http_client:
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
                            name=ns.name,
                            price=ns.price,
                            document=ns.document,
                            description=ns.description,
                            origin=ns.origin,
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
