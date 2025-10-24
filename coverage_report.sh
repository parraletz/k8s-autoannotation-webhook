#!/bin/bash
export PYTHONPATH=.

echo "Running comprehensive coverage analysis..."
echo ""

# Run tests with coverage
uv run pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=90

echo ""
echo "Coverage Analysis Complete!"
echo ""
echo "Reports generated:"
echo "  HTML: htmlcov/index.html"
echo "  XML:  coverage.xml"
echo "  Terminal: shown above"
echo ""
echo "View HTML report: open htmlcov/index.html"
echo "Minimum coverage threshold: 90%"
