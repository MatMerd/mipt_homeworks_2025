# GitHub Repository Search Service

FastAPI сервис для поиска GitHub репозиториев и экспорта результатов в CSV.

## Быстрый старт

```bash
# Установка зависимостей
pip install -e .

# Настройка (опционально)
cp .env.example .env
# Добавить GITHUB_TOKEN для увеличения лимита запросов

# Запуск
make run
```

Сервис будет доступен на http://localhost:8000

API документация: http://localhost:8000/docs
