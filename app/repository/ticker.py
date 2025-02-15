from typing import Any, Iterable, Sequence

from sqlalchemy import text
from sqlmodel import select

from app.common.db import AsyncSession, create_engine
from app.model.ticker import Ticker as Ticker


async def create_all(
    session: AsyncSession, tickers: Iterable[Ticker]
) -> Iterable[Ticker]:
    session.add_all(tickers)
    return tickers


async def truncate():
    async with create_engine().connect() as conn:
        statement = text("TRUNCATE TABLE ticker")
        conn.execute(statement)


async def get_all(session: AsyncSession, **kwargs: Any) -> Sequence[Ticker]:
    statement = select(Ticker).filter_by(**kwargs)
    result = await session.exec(statement)
    return result.fetchall()
