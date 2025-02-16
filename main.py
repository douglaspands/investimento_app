import sys
from pathlib import Path

if Path(sys.argv[0]).name in ("typer", "main.py", "trader", "trader.exe"):
    from app.cli import create_app

    app = create_app()

    if __name__ == "__main__":
        app()

else:
    print("This script is intended to be run as a Typer CLI application.")
    sys.exit(1)
