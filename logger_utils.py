import logging
import functools
import sys
from typing import Optional, Callable, Any

def log_errors(logger: Optional[logging.Logger] = None):
    def decorator(func: Callable[..., Any]):
        local_logger = logger
        if local_logger is None:
            local_logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                local_logger.error(
                    f"Ошибка в функции {func.__name__}: {e}", 
                    exc_info=True
                )
                raise e
        return wrapper
    return decorator