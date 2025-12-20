RUN := $(shell command -v uv >/dev/null 2>&1 && echo "uv run" || echo "")

SRC := github_stars

.PHONY: format format-check ruff mypy pyrefly test lint lint-check run

format:
	$(RUN) ruff format $(SRC)

format-check:
	$(RUN) ruff format $(SRC) --check

ruff:
	$(RUN) ruff check $(SRC)

mypy:
	$(RUN) mypy $(SRC)

pyrefly:
	$(RUN) pyrefly check $(SRC)

test:
	$(RUN) pytest -q

lint: format-check ruff mypy pyrefly

lint-check: lint test

run:
	$(RUN) -m github_stars
