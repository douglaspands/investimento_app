from app.resource.stock import Stock
from app.scraping import stock as stock_scraping


async def get_stock(ticker: str) -> Stock:
    """Get stock information.

    Args:
        ticker (str): Stock ticker.

    Returns:
        Stock: Stock information.
    """
    return await stock_scraping.get_stock(ticker=ticker)


async def list_stocks(tickers: list[str]) -> list[Stock]:
    """
    List stocks information.

    Args:
        tickers (list[str]): List of stock tickers.

    Returns:
        list[Stock]: List of Stock datas.
    """
    return await stock_scraping.list_stocks(tickers=tickers)


async def list_stocks_most_popular() -> list[Stock]:
    """
    Get most popular stocks information.

    Returns:
        list[Stock]: List of Stock datas.
    """
    return await stock_scraping.list_stocks_most_popular()
