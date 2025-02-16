from typing import Any, Iterable, Sequence

from sqlalchemy import text
from sqlmodel import select

from app.common.db import AsyncSession, create_engine
from app.model.ticker import Ticker as Ticker


async def create_all(session: AsyncSession, tickers: Iterable[Ticker]):
    """
    Inserts tickers into the database.

    Args:
        session (AsyncSession): DB Session.
        tickers (Iterable[Ticker]): List of the tickers to insert.
    """
    session.add_all(tickers)


async def get_all(session: AsyncSession, **kwargs: Any) -> Sequence[Ticker]:
    """
    Returns all tickers from the database.

    Args:
        session (AsyncSession): DB Session.

    Returns:
        Sequence[Ticker]: List of tickers.
    """
    statement = select(Ticker).filter_by(**kwargs)
    result = await session.exec(statement)
    return result.fetchall()


async def truncate():
    """
    Truncates the tickers table.
    """
    async with create_engine().connect() as conn:
        statement = text("DELETE FROM ticker")
        await conn.execute(statement)
        statement = text("COMMIT")
        await conn.execute(statement)
    async with create_engine().connect() as conn:
        statement = text("VACUUM")
        await conn.execute(statement)
