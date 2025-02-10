from typing import Any, Sequence

from sqlmodel import select

from app.common import utils
from app.common.database import AsyncSession
from app.model.stock import Stock as StockModel


async def get_all(
    session: AsyncSession, limit: int = 250, **values: Any
) -> Sequence[StockModel]:
    statement = select(StockModel).filter_by(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def get_by_ticker(session: AsyncSession, ticker: str) -> StockModel:
    statement = select(StockModel).where(StockModel.ticker == ticker)
    result = await session.exec(statement)
    return result.one()


async def create(session: AsyncSession, stock: StockModel) -> StockModel:
    session.add(stock)
    return stock


async def update_by_ticker(
    session: AsyncSession, ticker: str, **values: Any
) -> StockModel:
    utils.repository_columns_can_update(values)
    stock = await get_by_ticker(session=session, ticker=ticker)
    stock.sqlmodel_update(values)
    session.add(stock)
    return stock


async def get_or_create(session: AsyncSession, stock: StockModel) -> StockModel:
    stock_ = await get_all(
        session=session,
        limit=1,
        ticker=stock.ticker,
    )
    if stock_:
        return stock_[0]
    return await create(session=session, stock=stock)
