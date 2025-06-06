from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Stock(BaseModel):
    ticker: str
    name: str
    document: str
    price: Decimal
    updated_at: datetime
    description: str
    origin: str
