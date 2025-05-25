from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Column, Field, SQLModel

from app.common.model.type import DateTimeWithTimeZone
from app.common.utils import now_utc


class Reit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True, unique=True)
    name: str
    document: str
    admin: str
    segment: str
    price: Decimal
    origin: str
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
