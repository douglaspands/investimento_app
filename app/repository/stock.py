from datetime import datetime
from typing import Any, Sequence

from sqlalchemy.exc import NoResultFound
from sqlmodel import or_, select

from app.common import utils
from app.common.database import AsyncSession
from app.model.stock import Stock as StockModel


async def get_all(
    session: AsyncSession, limit: int = 250, **values: Any
) -> Sequence[StockModel]:
    statement = select(StockModel).filter_by(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def create(session: AsyncSession, stock: StockModel) -> StockModel:
    session.add(stock)
    return stock


async def get_by_ticker(session: AsyncSession, ticker: str) -> StockModel | None:
    statement = select(StockModel).where(StockModel.ticker == ticker)
    result = await session.exec(statement)
    return result.one_or_none()


async def get_all_by_tickers(
    session: AsyncSession, tickers: list[str], updated_at: datetime
) -> Sequence[StockModel]:
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
    utils.repository_columns_can_update(values)
    stock = await get_by_ticker(session=session, ticker=ticker)
    if not stock:
        raise NoResultFound("No row was found when one was required")
    stock.sqlmodel_update(values)
    session.add(stock)
    return stock
