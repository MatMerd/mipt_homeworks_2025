.PHONY: install run lint lint-check format clean

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	flake8 app/ --max-line-length=88 --extend-ignore=E203,W503

lint-check: lint

format:
	black app/ --line-length=88

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf static/*.csv