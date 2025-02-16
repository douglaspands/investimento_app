from functools import cache

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_config


@cache
def create_engine() -> AsyncEngine:
    config = get_config()
    return create_async_engine(
        url=str(config.db_url),
        echo=config.db_debug,
    )


@cache
def session_maker() -> async_sessionmaker[AsyncSession]:
    session_local = async_sessionmaker(
        bind=create_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_local
