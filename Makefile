.PHONY: install run lint lint-check format test

install:
	pip install -e ".[dev]"

run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

lint:
	ruff check src --fix
	ruff format src

lint-check:
	ruff check src
	ruff format src --check

format:
	ruff format src

test:
	pytest tests -v
