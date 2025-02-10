from typing import Any, Sequence

from sqlmodel import select

from app.common import utils
from app.common.database import AsyncSession
from app.model.reit import Reit as ReitModel


async def get_all(
    session: AsyncSession, limit: int = 250, **values: Any
) -> Sequence[ReitModel]:
    statement = select(ReitModel).filter_by(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def get_by_ticker(session: AsyncSession, ticker: str) -> ReitModel:
    statement = select(ReitModel).where(ReitModel.ticker == ticker)
    result = await session.exec(statement)
    return result.one()


async def create(session: AsyncSession, reit: ReitModel) -> ReitModel:
    session.add(reit)
    return reit


async def update_by_ticker(
    session: AsyncSession, ticker: str, **values: Any
) -> ReitModel:
    utils.repository_columns_can_update(values)
    reit = await get_by_ticker(session=session, ticker=ticker)
    reit.sqlmodel_update(values)
    session.add(reit)
    return reit


async def get_or_create(session: AsyncSession, reit: ReitModel) -> ReitModel:
    reit_ = await get_all(
        session=session,
        limit=1,
        ticker=reit.ticker,
    )
    if reit_:
        return reit_[0]
    return await create(session=session, reit=reit)
