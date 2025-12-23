import logging
import functools
from typing import Optional, Callable, Any

def log_errors(logger: Optional[logging.Logger] = None):
    """
    Декоратор, который логирует ошибки. 
    Принимает опциональный объект логгера.
    """
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                current_logger = logger if logger is not None else logging.getLogger(func.__module__)
                
                current_logger.error(f"Ошибка в функции {func.__name__}: {e}", exc_info=True)
                
                raise e
        return wrapper
    return decorator