# Ответы на вопросы

## Проблема создания httpx.AsyncClient на каждый вызов метода

```python
async with httpx.AsyncClient() as client:
    response = await client.get(...)
```

Создание нового `httpx.AsyncClient` на каждый вызов метода имеет недостатки:

1. Каждый раз создаётся новое TCP соединение к серверу GitHub API. Это требует:
   - DNS lookup
   - TCP handshake (3-way handshake)
   - TLS handshake (для HTTPS) - особенно затратная операция

2. **Отсутствие connection pooling**: `httpx.AsyncClient` поддерживает пул соединений (HTTP/2 multiplexing и HTTP/1.1 keep-alive). При создании клиента на каждый запрос эта оптимизация не используется.

3. **Накладные расходы на инициализацию**: Создание объекта клиента включает инициализацию транспортного слоя, настройку таймаутов, headers и других параметров.

### Рекомендуемое решение

Использовать один экземпляр `AsyncClient` на время жизни приложения или на время жизни запроса:

```python
class GitHubClient:
    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            headers=self._build_headers(token),
            timeout=30.0,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def search_repositories(self, search_params: GitHubSearchParams) -> dict[str, Any]:
        response = await self._client.get(
            f"{self.base_url}/search/repositories",
            params={...},
        )
        response.raise_for_status()
        return response.json()
```

И управлять жизненным циклом через FastAPI lifespan:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown - закрытие клиента
    await github_client.close()
```

### P. S.

Это не критично сейчас если:
- Количество запросов небольшое
- Сервис не под высокой нагрузкой
