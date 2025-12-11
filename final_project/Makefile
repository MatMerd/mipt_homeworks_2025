.PHONY: install lint lint-check format run test clean

install:
	pip install -e ".[dev]"

lint-check:
	ruff check app/
	ruff format --check app/
	mypy app/

lint:
	ruff check --fix app/
	ruff format app/

format:
	ruff format app/

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
