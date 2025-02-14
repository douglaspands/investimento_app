from datetime import datetime
from typing import Any, Sequence

from sqlalchemy.exc import NoResultFound
from sqlmodel import or_, select

from app.common import utils
from app.common.db import AsyncSession
from app.model.reit import Reit as ReitModel


async def create(session: AsyncSession, reit: ReitModel) -> ReitModel:
    session.add(reit)
    return reit


async def get_by_ticker(session: AsyncSession, ticker: str) -> ReitModel | None:
    statement = select(ReitModel).where(ReitModel.ticker == ticker)
    result = await session.exec(statement)
    return result.one_or_none()


async def get_all_by_tickers(
    session: AsyncSession, tickers: list[str], updated_at: datetime
) -> Sequence[ReitModel]:
    statement = (
        select(ReitModel)
        .where(or_(*[ReitModel.ticker == ticker for ticker in tickers]))
        .where(ReitModel.updated_at >= updated_at)
    )
    result = await session.exec(statement)
    return result.all()


async def update_by_ticker(
    session: AsyncSession, ticker: str, **values: Any
) -> ReitModel:
    utils.repository_columns_can_update(values)
    reit = await get_by_ticker(session=session, ticker=ticker)
    if not reit:
        raise NoResultFound("No row was found when one was required")
    reit.sqlmodel_update(values)
    session.add(reit)
    return reit
