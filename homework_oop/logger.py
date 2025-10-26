def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f" Выполняется {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            print(f" {func.__name__} успешно завершена")
            return result
        except Exception as e:
            print(f" Ошибка в {func.__name__}: {e}")
            raise
    return wrapper