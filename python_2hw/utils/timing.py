import time
import inspect
import functools
import logging
from typing import Callable, Optional

logger = logging.getLogger("timing")

def measure_time(name: Optional[str] = None, log: Optional[logging.Logger] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        is_coroutine = inspect.iscoroutinefunction(func)
        target_logger = log or logger

        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    elapsed = time.perf_counter() - start
                    metric = name or f"{func.__module__}.{func.__qualname__}"
                    target_logger.info("%s executed in %.3f s", metric, elapsed)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    elapsed = time.perf_counter() - start
                    metric = name or f"{func.__module__}.{func.__qualname__}"
                    target_logger.info("%s executed in %.3f s", metric, elapsed)
            return sync_wrapper

    return decorator