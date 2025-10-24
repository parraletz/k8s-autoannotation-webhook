.PHONY: test coverage coverage-html coverage-report clean install run help

# Default target
help:
	@echo "FastAPI Template Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install     Install dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test        Run tests"
	@echo "  coverage    Run tests with coverage"
	@echo "  coverage-html Run tests with HTML coverage report"
	@echo "  coverage-report Comprehensive coverage analysis"
	@echo ""
	@echo "Running:"
	@echo "  run         Start the development server"
	@echo "  run-prod    Start the production server"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean       Remove coverage files and cache"

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
	@uv run python main.py

clean:
	@echo "Cleaning up..."
	@rm -rf htmlcov/
	@rm -f .coverage coverage.xml
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .pytest_cache -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"
