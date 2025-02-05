from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Reit(BaseModel):
    ticker: str
    name: str
    admin: str
    segment: str
    price: Decimal
    updated_at: datetime
