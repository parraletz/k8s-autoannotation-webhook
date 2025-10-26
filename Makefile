.PHONY: test coverage coverage-html coverage-report clean install run help pre-commit-install pre-commit-run lint format security

# Default target
help:
	@echo "Kubernetes Webhook Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install            Install dependencies"
	@echo "  pre-commit-install Install pre-commit hooks"
	@echo ""
	@echo "Code Quality:"
	@echo "  format             Format code with black and isort"
	@echo "  lint               Run linting checks"
	@echo "  security           Run security scans (bandit, pip-audit)"
	@echo "  pre-commit-run     Run all pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  test               Run tests"
	@echo "  coverage           Run tests with coverage"
	@echo "  coverage-html      Run tests with HTML coverage report"
	@echo "  coverage-report    Comprehensive coverage analysis"
	@echo ""
	@echo "Running:"
	@echo "  run                Start the development server"
	@echo "  run-prod           Start the production server"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean              Remove coverage files and cache"

install:
	uv sync

test:
	@export PYTHONPATH=. && uv run pytest -v

coverage:
	@export PYTHONPATH=. && uv run pytest --cov=app --cov-report=term-missing

coverage-html:
	@./run_coverage.sh

coverage-report:
	@./coverage_report.sh

run:
	@export ENVIRONMENT=local && uv run python main.py

run-prod:
	@export HOST=0.0.0.0 && export ENVIRONMENT=production && uv run python main.py

clean:
	@echo "Cleaning up..."
	@rm -rf htmlcov/
	@rm -f .coverage coverage.xml
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .pytest_cache -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

# Pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	@uv run pre-commit install
	@uv run pre-commit install --hook-type commit-msg
	@echo "Pre-commit hooks installed!"

pre-commit-run:
	@echo "Running pre-commit hooks on all files..."
	@uv run pre-commit run --all-files

# Code formatting and linting
format:
	@echo "Formatting code..."
	@uv run black app/ tests/
	@uv run isort app/ tests/
	@echo "Code formatted!"

lint:
	@echo "Running linting checks..."
	@uv run flake8 app/ tests/
	@uv run mypy app/
	@echo "Linting complete!"

security:
	@echo "Running security checks..."
	@uv run bandit -r app/
	@uv run pip-audit
	@echo "Security checks complete!"
