from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel

from app.common.utils import now_utc


class Stock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True, unique=True)
    name: str
    description: str
    document: str
    price: Decimal
    origin: str
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: now_utc(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: now_utc(),
            onupdate=lambda: now_utc(),
            nullable=False,
        )
    )
