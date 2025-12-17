# fastapi_homework

Работу выполнили Корнилов Анатолий, Мызников Александр

This project was generated using fastapi_template.

## UV

This project uses uv. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
python -m uvicorn homework_fastapi.main:app --reload
```

This will start the server on the configured host.

You can find swagger documentation at `/docs`.

Линтеры:
```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

Примеры запросов для тестирования:

# 1. Минимальный обязательный запрос
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Python"

# 2. Базовый запрос с лимитом
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=JavaScript&limit=5"

# 3. Запрос с пагинацией (offset)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Java&limit=10&offset=20"

# 4. Фильтр по звёздам (только минимум)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Go&stars_min=1000&limit=8"

# 5. Фильтр по звёздам (диапазон)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Rust&stars_min=500&stars_max=5000&limit=6"

# 6. Фильтр по форкам (только минимум)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=TypeScript&forks_min=100&limit=12"

# 7. Фильтр по форкам (диапазон)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=C%2B%2B&forks_min=50&forks_max=500&limit=15"

# 8. Комбинированные фильтры (звёзды + форки)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Kotlin&stars_min=100&forks_min=10&limit=7"

# 9. Все параметры вместе
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Swift&limit=25&offset=5&stars_min=200&stars_max=10000&forks_min=30&forks_max=1000"

# 10. Максимальный лимит (проверка граничного значения)
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/repositories/search?lang=Python&limit=1000&stars_min=10000"
