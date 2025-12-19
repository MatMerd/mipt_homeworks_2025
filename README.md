# GitFastApi

## Установка зависимостей

```bash
pip install fastapi uvicorn httpx aiofile
```

## Запуск

```bash
python -m uvicorn gitfastapi.main:app --reload
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

### API

### Endpoint: `GET /repos/save`

#### Параметры:
- `limit` (int): Количество репозиториев (обязательно).
- `lang` (str): Язык программирования (обязательно).
- `offset` (int): Смещение (по умолчанию 0).
- `stars_min` (int): Минимальное кол-во звезд.
- `stars_max` (int): Максимальное кол-во звезд.
- `forks_min` (int): Минимальное кол-во форков.
- `forks_max` (int): Максимальное кол-во форков.


### Проверка линтерами:

```bash
make lint-check
```
