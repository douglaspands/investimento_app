from datetime import datetime
from typing import Any, Sequence

from sqlalchemy.exc import NoResultFound
from sqlmodel import or_, select

from app.common import utils
from app.common.db import AsyncSession
from app.common.utils import now_utc
from app.model.stock import Stock as StockModel


async def create(session: AsyncSession, stock: StockModel) -> StockModel:
    """
    Create a new stock record.

    Args:
        session: The database session.
        stock: The stock record to create.

    Returns:
       The created stock record.
    """
    session.add(stock)
    return stock


async def get_by_ticker(session: AsyncSession, ticker: str) -> StockModel | None:
    """
    Get a stock record by its ticker.
    Args:
        session: The database session.
        ticker: The stock's ticker.
    Returns:
       The stock record if found, otherwise None.
    """
    statement = select(StockModel).where(StockModel.ticker == ticker)
    result = await session.exec(statement)
    return result.one_or_none()


async def get_all_by_tickers(
    session: AsyncSession, tickers: list[str], updated_at: datetime
) -> Sequence[StockModel]:
    """
    Get all stock records by their tickers.
    Args:
        session: The database session.
        tickers: A list of stock tickers.
        updated_at: The last update time to filter the stocks.
    Returns:
       A list of stock records that match the tickers and updated_at time.
    """
    statement = (
        select(StockModel)
        .where(or_(*[StockModel.ticker == ticker for ticker in tickers]))
        .where(StockModel.updated_at >= updated_at)
    )
    result = await session.exec(statement)
    return result.all()


async def update_by_ticker(
    session: AsyncSession, ticker: str, **values: Any
) -> StockModel:
    """
    Update a stock record by its ticker.
    Args:
        session: The database session.
        ticker: The stock ticker.
        **values: The values to update.
    Returns:
       The updated stock record.
    """
    values["updated_at"] = now_utc()
    utils.repository_columns_can_update(values)
    stock = await get_by_ticker(session=session, ticker=ticker)
    if not stock:
        raise NoResultFound("No row was found when one was required")
    stock.sqlmodel_update(values)
    session.add(stock)
    return stock
