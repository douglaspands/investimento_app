import os
from functools import cache
from pathlib import Path

import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    name: str
    description: str
    version: str

    db_url: str
    db_debug: bool = False

    alembic_ini: Path
    alembic_migration_folder: Path

    stock_cache_ttl: int = 10 * 60
    reit_cache_ttl: int = 10 * 60

    root_path: Path
    config_path: Path

    scraping_timeout_ttl: float = (1 * 60) + 0.001

    timezone_local: str = "America/Sao_Paulo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@cache
def get_config():
    root_path = Path(__file__).parent.parent
    alembic_ini = root_path / "alembic.ini"
    alembic_migration_folder = root_path / "migration"
    db_url = "sqlite+aiosqlite:///db.sqlite3"

    with root_path.joinpath("pyproject.toml").open("rb") as f:
        config = tomllib.load(f)

    if os.getenv("BIN_EXE") == "1":
        config_path = Path.home().joinpath(".trader")
        config_path.mkdir(parents=True, exist_ok=True)

    else:
        config_path = root_path

    return Config(
        name=config["project"]["name"],
        description=config["project"]["description"],
        version=config["project"]["version"],
        db_url=db_url,
        root_path=root_path,
        config_path=config_path,
        alembic_ini=alembic_ini,
        alembic_migration_folder=alembic_migration_folder,
    )
