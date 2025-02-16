from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, SQLModel

from app.common.model.type import DateTimeWithTimeZone
from app.common.utils import now_utc
from app.enum.ticker import TickerTypeEnum


class Ticker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, unique=True)
    help: str
    type: TickerTypeEnum = Field(index=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTimeWithTimeZone,
            default=lambda: now_utc(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTimeWithTimeZone,
            default=lambda: now_utc(),
            onupdate=lambda: now_utc(),
            nullable=False,
        )
    )
