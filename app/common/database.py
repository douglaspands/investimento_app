from functools import cache

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_config


@cache
def db_session_maker() -> async_sessionmaker[AsyncSession]:
    config = get_config()
    session_local = async_sessionmaker(
        bind=create_async_engine(
            url=str(config.db_url),
            echo=config.db_debug,
        ),
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_local
