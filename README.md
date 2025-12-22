# GitHub Repositories Export (FastAPI)

Сервис делает **одну ручку**, которая ходит в GitHub Search API, ищет репозитории по фильтрам и **сохраняет результат в CSV** в папку `static/`.

CSV создаётся по пути:

- `github_stars/static/repositories_{lang}_{limit}_{offset}.csv`

> Файл **перезаписывается**, если вызвать ручку с теми же `lang/limit/offset`.

---

## Требования
    
- Python **3.12+** (в проекте `requires-python = ">=3.12, <4.0"`)
- Установленный **uv** (рекомендуется)
- (Опционально) GitHub token для увеличения лимитов API:
  - переменная окружения: `GITHUB_TOKEN`

---

## Установка и запуск локально

### 1) Установить зависимости
Из папки `github_stars/`:

```bash
cd github_stars
uv sync --locked
```

### 2) Запустить сервис
Вариант A (из `github_stars/`):

```bash
uv run -m github_stars
```

Вариант B (из корня репозитория):

```bash
uv run make run
```

После запуска сервис доступен на:

- `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/api/docs`

---

## Настройка GitHub токена (рекомендуется, но можно и не делать)

### macOS/Linux
```bash
export GITHUB_TOKEN="ghp_***"
```

После этого нужно перезапустить программу

---

## Линтеры и тесты (локально)

Из корня репозитория:

```bash
uv run make lint-check
```

Или из `github_stars/`:

```bash
cd github_stars
uv run make lint-check
```

Полезные команды:

```bash
uv run make format
uv run make format-check
uv run make ruff
uv run make mypy
uv run make pyrefly
uv run make test
```

---

## Endpoint

`GET /api/github-repos/export`

### Query параметры
- `limit` — сколько репозиториев вернуть
- `offset` — смещение (сколько пропустить)
- `lang` — язык репозитория (например `Go`, `Python`, `JavaScript`)
- `stars_min` — минимум звёзд (по умолчанию 0)
- `stars_max` — максимум звёзд (если не задан — без ограничения)
- `forks_min` — минимум форков (по умолчанию 0)
- `forks_max` — максимум форков (если не задан — без ограничения)
- `sort` — `stars | forks | updated` (по умолчанию `stars`)
- `order` — `asc | desc` (по умолчанию `desc`)

---

## 10 разных примеров curl

### 1) Базовый (минимум параметров)
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=20&offset=0&lang=Python"
```

### 2) С диапазоном stars и forks
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=20&offset=5&lang=Go&stars_min=50&stars_max=5000&forks_min=10&forks_max=2000"
```

### 3) Только минимум звёзд, без stars_max
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=30&offset=0&lang=JavaScript&stars_min=20000"
```

### 4) Только минимум форков, без forks_max
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=15&offset=0&lang=TypeScript&forks_min=5000"
```

### 5) Сортировка по звёздам (явно)
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=10&offset=0&lang=Rust&stars_min=1000&sort=stars&order=desc"
```

### 6) Сортировка по форкам
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=10&offset=0&lang=Kotlin&stars_min=500&sort=forks&order=desc"
```

### 7) Самые недавно обновлённые (свежие сверху)
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=20&offset=0&lang=Go&stars_min=50&forks_min=10&sort=updated&order=desc"
```

### 8) Самые давно обновлённые (старые сверху)
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=20&offset=0&lang=Go&stars_min=50&forks_min=10&sort=updated&order=asc"
```

### 9) Проверка пагинации: offset не кратен 100
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=25&offset=123&lang=Python&stars_min=1000&sort=stars&order=desc"
```

### 10) Пример с “ошибкой валидации” (stars_min > stars_max)
Ожидаемо вернёт ошибку (валидация диапазона):
```bash
curl "http://127.0.0.1:8000/api/github-repos/export?limit=10&offset=0&lang=Python&stars_min=5000&stars_max=10"
```
