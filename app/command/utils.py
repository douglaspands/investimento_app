from rich.console import Console
from typer import Typer

from app.common import aio
from app.service import ticker as ticker_service

app = Typer(name="utils", help="General utils.")
console = Console()


@app.command("auto_complete", help="Download of the autocomplete.")
def tickers_download():
    aio.run(ticker_service.save_all_tickers())
    console.print("Tickers downloaded successfully!")
