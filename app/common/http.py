from functools import cache

from httpx import AsyncClient


@cache
def get_httpclient() -> AsyncClient:
    return AsyncClient()
