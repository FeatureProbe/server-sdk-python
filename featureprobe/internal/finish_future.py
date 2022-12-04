import asyncio


def finish_future(func):
    """Fires async functions without waiting it for finish."""
    def wrapped(*args, **kwargs):
        return asyncio.run_coroutine_threadsafe(func(*args, **kwargs), asyncio.get_event_loop())

    return wrapped


@finish_future
async def aaa(n):
    for i in range(n):
        print(i)
