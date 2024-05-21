.PHONY: test install

test:
	poetry run pytest -vv tests \
	--cov=. \
	--cov-report=term \
	 --cov-report=xml:coverage.xml   

install:
	poetry install

format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8 src/autonotellm
	poetry run mypy src/autonotellm