from app.common.db import session_maker
from app.common.http import get_client
from app.enum.ticker import TickerTypeEnum
from app.model.ticker import Ticker as TickerModel
from app.repository import ticker as ticker_repository
from app.resource.ticker import Ticker
from app.scraping.dados_de_mercado.stock import DadosDeMercadoStockScraping

SessionLocal = session_maker()


async def list_tickers(type: TickerTypeEnum) -> list[Ticker]:
    """
    List all available tickers.

    Args:
        type (TickerTypeEnum): Type of ticker to list.

    Returns:
        list[str]: List of tickers.
    """
    async with SessionLocal() as db_session:
        tickers = await ticker_repository.get_all(session=db_session, type=type)
    return [Ticker(**t.__dict__) for t in tickers]


async def save_all_tickers():
    """
    Save all available tickers to the database.
    """
    async with get_client() as http_client:
        stock_scraping = DadosDeMercadoStockScraping(client=http_client)
        tickers = await stock_scraping.list_tickers()
        await ticker_repository.truncate()
        async with SessionLocal() as db_session, db_session.begin():
            await ticker_repository.create_all(
                session=db_session, tickers=[TickerModel(**t.__dict__) for t in tickers]
            )
