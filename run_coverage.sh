#!/bin/bash
export PYTHONPATH=.

echo "🧪 Running tests with coverage..."
uv run pytest --cov=app --cov-report=term-missing --cov-report=html "$@"

echo ""
echo "📊 Coverage report generated!"
echo "📁 HTML report: htmlcov/index.html"
echo "🌐 Open with: open htmlcov/index.html"
