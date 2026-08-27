.PHONY: help bot unit black flake8 ruff

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  make bot     - run the bot locally"
	@echo "  make unit    - run unit tests with coverage"
	@echo "  make black   - format code with black"
	@echo "  make flake8  - lint code with flake8"
	@echo "  make ruff    - lint code with ruff"

bot:
	uv run python main.py

unit:
	uv run pytest tests/test_fast --cov=src --cov-report=term-missing --cov-fail-under=90

black:
	uv run black main.py src tests

flake8:
	uv run flake8 main.py src tests

ruff:
	uv run ruff check main.py src tests
