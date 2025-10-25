SRC_FOLDERS=$(wildcard homework_*)
TEST_FOLDERS=$(wildcard homework_*/tests)

lint:
	ruff check $(SRC_FOLDERS)
	mypy $(SRC_FOLDERS)
	@make lint-format

format:
	ruff format $(SRC_FOLDERS)

fix:
	ruff check $(SRC_FOLDERS) --fix

lint-format:
	ruff format $(SRC_FOLDERS) --check

tests:
	pytest -v --disable-warnings --maxfail=1 $(TEST_FOLDERS)
