import asyncio
from functools import cache
from typing import Coroutine


@cache
def get_loop():
    return asyncio.new_event_loop()


def run(coroutine: Coroutine):
    return get_loop().run_until_complete(coroutine)
