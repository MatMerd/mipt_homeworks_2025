# final_project

Итоговая работа по курсу Python: FastAPI‑сервис с одной ручкой, которая ищет GitHub‑репозитории через `search/repositories` и сохраняет результат в CSV.

## UV

This project uses uv. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
uv sync --locked
uv run -m final_project
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## Final homework endpoint

`GET /api/repositories/search`

Query parameters:
- `limit` (required)
- `offset` (default: 0)
- `lang` (required)
- `stars_min` (default: 0)
- `stars_max` (default: unlimited)
- `forks_min` (default: 0)
- `forks_max` (default: unlimited)

Result: CSV file is created in `final_project/static` with name `repositories_{lang}_{limit}_{offset}.csv`.

You can read more about uv here: https://docs.astral.sh/ruff/

## Docker

You can start the project with docker using this command:

```bash
docker-compose up --build
```

If you want to develop in docker with autoreload and exposed ports add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `uv.lock` or `pyproject.toml` with this command:

```bash
docker-compose build
```

## Project structure

```bash
$ tree "final_project"
final_project
├── conftest.py  # Fixtures for all tests.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifespan.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "FINAL_PROJECT_" prefix.

For example if you see in your "final_project/settings.py" a variable named like
`random_parameter`, you should provide the "FINAL_PROJECT_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `final_project.settings.Settings.Config`.

An example of .env file:
```bash
FINAL_PROJECT_RELOAD="True"
FINAL_PROJECT_PORT="8000"
FINAL_PROJECT_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* mypy (validates types);
* ruff (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv .
docker-compose down
```

For running tests on your local machine.


2. Run the pytest.
```bash
pytest -vv .
```

## Как запустить и проверить

```bash
uv sync --locked
make serve
```

Swagger: `http://127.0.0.1:8000/api/docs`

Example request:

```bash
curl -sS "http://127.0.0.1:8000/api/repositories/search?limit=5&offset=0&lang=Python&stars_min=100&forks_min=0"
```

The CSV will appear in `final_project/static/`:

```bash
ls -la final_project/static
```

## Checks (lint + unit)

```bash
make test
```
