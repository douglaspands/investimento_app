from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


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
            DateTime,
            default=lambda: datetime.now(tz=timezone.utc),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(tz=timezone.utc),
            onupdate=lambda: datetime.now(tz=timezone.utc),
            nullable=False,
        )
    )
