SHELL:=/usr/bin/env bash

.PHONY: serve
serve:
	uv run -m final_project

.PHONY: lint
lint:
	uv run ruff check --exit-non-zero-on-fix
	uv run ruff format --check --diff
	uv run python -m mypy ${PWD}

.PHONY: format
format:
	uv run ruff format

.PHONY: unit
unit:
	uv run python -m pytest

.PHONY: package
package:
	uv run pip check

.PHONY: test
test: lint unit

