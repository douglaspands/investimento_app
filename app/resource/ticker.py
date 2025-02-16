from pydantic import BaseModel

from app.enum.ticker import TickerTypeEnum


class Ticker(BaseModel):
    symbol: str
    help: str
    type: TickerTypeEnum
