.PHONY: help install test lint format type-check clean build publish docs dev

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	poetry install

dev: install ## Install development dependencies
	poetry run pre-commit install

test: ## Run tests with coverage
	poetry run pytest --cov=bearing --cov-report=term-missing --cov-report=html tst/

test-fast: ## Run tests without coverage
	poetry run pytest tst/

lint: ## Run linters
	poetry run flake8 src/ --max-line-length=88 --extend-ignore=E203,W503
	poetry run isort --check-only --profile black src/
	poetry run black --check src/

format: ## Format code with black and isort
	poetry run black src/ tst/
	poetry run isort --profile black src/ tst/

type-check: ## Run type checking with mypy
	poetry run mypy src/bearing --ignore-missing-imports

clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

build: clean ## Build distribution packages
	poetry build

publish: build ## Publish to PyPI
	poetry publish

publish-test: build ## Publish to Test PyPI
	poetry publish --repository testpypi

docs: ## Build documentation
	cd docs && poetry run mkdocs build

docs-serve: ## Serve documentation locally
	cd docs && poetry run mkdocs serve

pre-commit: ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

update: ## Update dependencies
	poetry update

lock: ## Update poetry.lock file
	poetry lock --no-update

check: lint type-check test ## Run all checks (lint, type-check, test)

.DEFAULT_GOAL := help
