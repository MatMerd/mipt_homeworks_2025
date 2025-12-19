
.PHONY: lint-check

lint-check:
	ruff check .
	mypy .
