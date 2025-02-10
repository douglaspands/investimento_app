from functools import cache

import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    name: str
    description: str
    version: str

    db_url: str = "sqlite+aiosqlite:///db.sqlite3"
    db_debug: bool = False

    stock_cache_ttl: int = 600
    reit_cache_ttl: int = 600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@cache
def get_config():
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    return Config(
        name=config["project"]["name"],
        description=config["project"]["description"],
        version=config["project"]["version"],
    )
