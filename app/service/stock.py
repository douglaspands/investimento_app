from datetime import datetime, timedelta

from app.common.database import db_session_maker
from app.common.http import get_httpclient
from app.model.stock import Stock as StockModel
from app.repository import stock as stock_repository
from app.resource.stock import Stock
from app.scraping import stock as stock_scraping

SessionLocal = db_session_maker()


async def get_stock(ticker: str) -> Stock:
    """Get stock information.

    Args:
        ticker (str): Stock ticker.

    Returns:
        Stock: Stock information.
    """
    async with SessionLocal() as db_session:
        async with get_httpclient() as http_client:
            stock = await stock_repository.get_by_ticker(
                session=db_session, ticker=ticker
            )
            if stock:
                if stock.updated_at and stock.updated_at < (
                    datetime.now() - timedelta(minutes=10)
                ):
                    stoke_now = await stock_scraping.get_stock(
                        ticker=ticker, client=http_client
                    )
                    stock.price = stoke_now.price
                    stock.updated_at = stoke_now.updated_at
                    await stock_repository.update_by_ticker(
                        session=db_session,
                        ticker=ticker,
                        price=stoke_now.price,
                        updated_at=stoke_now.updated_at,
                    )
            else:
                stoke_now = await stock_scraping.get_stock(
                    ticker=ticker, client=http_client
                )
                stock = await stock_repository.create(
                    session=db_session, stock=StockModel(**stoke_now.__dict__)
                )
    return Stock(**stock.__dict__)


async def list_stocks(tickers: list[str]) -> list[Stock]:
    """
    List stocks information.

    Args:
        tickers (list[str]): List of stock tickers.

    Returns:
        list[Stock]: List of Stock datas.
    """
    async with get_httpclient() as http_client:
        return await stock_scraping.list_stocks(client=http_client, tickers=tickers)


async def list_stocks_most_popular() -> list[Stock]:
    """
    Get most popular stocks information.

    Returns:
        list[Stock]: List of Stock datas.
    """
    async with get_httpclient() as http_client:
        return await stock_scraping.list_stocks_most_popular(client=http_client)
