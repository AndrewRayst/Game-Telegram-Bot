from time import sleep
from typing import Callable


def exponential_backoff(
        min_delay: int = 100,
        max_delay: int = 15000,
        factor: int = 2) -> Callable:

    exponential_backoff.delay = min_delay

    def _exponential_backoff(func: Callable) -> Callable:
        def wrapped_func(*args, **kwargs) -> any:
            while True:
                response = func(*args, **kwargs)
                if response:
                    return response

                sleep(exponential_backoff.delay / 3600)

                exponential_backoff.delay *= factor

                if exponential_backoff.delay > max_delay:
                    break

        return wrapped_func

    return _exponential_backoff
