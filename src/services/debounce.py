from asyncio import get_running_loop
from functools import wraps
from typing import Callable, TypeVar, Coroutine


def debounce(wait_time: float):
    """
    Decorator that will debounce a function so that it is called after wait_time seconds
    If it is called multiple times, will wait for the last call to be debounced and run only this one.

    To get debounce result, you need to await resulting function!
    """
    return_type = TypeVar("return_type")

    def decorator(function: Callable[..., return_type]) -> Callable[..., Coroutine[..., ..., return_type]]:
        @wraps(function)
        async def debounced(*args, **kwargs) -> return_type:
            loop = get_running_loop()
            fut = loop.create_future()

            def call_function():
                debounced.timer = None
                fut.set_result(function(*args, **kwargs))

            if debounced.timer is not None:
                debounced.timer.cancel()

            debounced.timer = loop.call_later(wait_time, call_function)

            return await fut

        debounced.timer = None
        return debounced

    return decorator
