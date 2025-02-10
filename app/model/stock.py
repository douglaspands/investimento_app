from datetime import datetime
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
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(),
            nullable=False,
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(),
            onupdate=lambda: datetime.now(),
            nullable=False,
        )
    )
