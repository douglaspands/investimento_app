from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


class Reit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True, unique=True)
    name: str
    admin: str
    segment: str
    price: Decimal
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
    )
