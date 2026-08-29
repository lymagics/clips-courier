.PHONY: help bot migrate forward apply rollback history unit black flake8 ruff

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  make bot                  - run the bot locally"
	@echo "  make migrate              - upgrade the database to the latest migration"
	@echo "  make forward              - upgrade the database by one migration"
	@echo "  make apply tag=<revision> - upgrade the database to a specific revision"
	@echo "  make rollback             - downgrade the database by one migration"
	@echo "  make history              - show the migration history"
	@echo "  make unit                 - run unit tests with coverage"
	@echo "  make black                - format code with black"
	@echo "  make flake8               - lint code with flake8"
	@echo "  make ruff                 - lint code with ruff"

bot:
	uv run python main.py

migrate:
	uv run alembic upgrade head

forward:
	uv run alembic upgrade +1

apply:
	uv run alembic upgrade $(tag)

rollback:
	uv run alembic downgrade -1

history:
	uv run alembic history --verbose

unit:
	uv run pytest tests/test_fast --cov=src --cov-report=term-missing --cov-fail-under=90

black:
	uv run black main.py src tests

flake8:
	uv run flake8 main.py src tests

ruff:
	uv run ruff check main.py src tests
