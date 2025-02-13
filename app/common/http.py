from httpx import AsyncClient


def get_httpclient() -> AsyncClient:
    return AsyncClient()
