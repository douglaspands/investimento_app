from app.common import aio
from app.enum.ticker import TickerTypeEnum
from app.service import ticker as stock_service


def complete_stock_tickers(incomplete: str) -> list[tuple[str, str]]:
    """
    Complete stock tickers.

    Args:
        incomplete (str): The incomplete ticker symbol.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the ticker symbol and help text.
    """
    completion = []
    for ticker in aio.run(stock_service.list_tickers(type=TickerTypeEnum.STOCK)):
        if ticker.symbol.startswith(incomplete):
            completion.append((ticker.symbol, ticker.help))
    return completion


def complete_reit_tickers(incomplete: str):
    """
    Complete REIT tickers.

    Args:
        incomplete (str): The incomplete ticker symbol.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the ticker symbol and help text.
    """
    completion = []
    for ticker in aio.run(stock_service.list_tickers(type=TickerTypeEnum.REIT)):
        if ticker.symbol.startswith(incomplete):
            completion.append((ticker.symbol, ticker.help))
    return completion
