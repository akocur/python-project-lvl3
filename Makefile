install:
	poetry install
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=page_loader
code-climate:
	poetry run pytest --cov=page_loader --cov-report xml
lint:
	poetry run flake8 page_loader
selfcheck:
	poetry check
check: selfcheck test lint

build: check
	poetry build

rec:
	poetry run asciinema rec

install-package: build
	python3 -m pip install --user .

.PHONY: install test lint selfcheck check build