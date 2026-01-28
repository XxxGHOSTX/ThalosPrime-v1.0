# Makefile for Thalos Prime Development

.PHONY: help install install-dev test test-cov lint format type-check clean build docs release

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in production mode
	pip install .

install-dev: ## Install package in development mode with all dependencies
	pip install -e ".[dev]"

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=thalos_prime --cov-report=html --cov-report=term

test-quick: ## Run tests without coverage
	pytest tests/ -x

lint: ## Run linter (flake8)
	flake8 src/thalos_prime tests/

format: ## Format code with Black
	black src/ tests/ examples/

format-check: ## Check code formatting without modifying
	black --check src/ tests/ examples/

type-check: ## Run type checker (mypy)
	mypy src/thalos_prime

isort: ## Sort imports
	isort src/ tests/ examples/

isort-check: ## Check import sorting
	isort --check-only src/ tests/ examples/

quality: format lint type-check ## Run all quality checks

clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

build: clean ## Build distribution packages
	python -m build

docs: ## Build documentation
	@echo "Documentation building not yet configured"
	@echo "Install sphinx and run: cd docs && make html"

publish-test: build ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI
	python -m twine upload dist/*

dev: install-dev ## Setup development environment
	@echo "Development environment ready!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make quality' to check code quality"

ci: format-check lint type-check test-cov ## Run all CI checks

verify: ## Verify installation
	python -c "import thalos_prime; print(f'Thalos Prime v{thalos_prime.__version__} installed successfully')"

.DEFAULT_GOAL := help
