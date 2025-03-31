from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, NonNegativeInt

from app.resource.reit import Reit
from app.resource.stock import Stock


class PurchaseBalance(BaseModel):
    stocks_balance: list[StockBalance]
    amount_invested: Decimal
    created_at: datetime

    @property
    def stock_count(self) -> int:
        return sum([sb.count for sb in self.stocks_balance])

    @property
    def amount_spent(self) -> Decimal:
        total = Decimal(0)
        for stock_balance in self.stocks_balance:
            total += stock_balance.total_amount
        return total

    @property
    def remaining_balance(self) -> Decimal:
        return self.amount_invested - self.amount_spent


class StockBalance(BaseModel):
    unit: Stock | Reit
    count: NonNegativeInt

    @property
    def total_amount(self) -> Decimal:
        return self.unit.price * self.count
