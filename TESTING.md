# 🧪 Testing & Coverage Guide

## Quick Start

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Generate HTML coverage report
make coverage-html

# Comprehensive coverage analysis
make coverage-report
```

## Coverage Commands

### 1. Basic Coverage

```bash
./run_tests.sh --cov=app
```

### 2. Coverage with HTML Report

```bash
./run_coverage.sh
```

### 3. Comprehensive Coverage Analysis

```bash
./coverage_report.sh
```

### 4. Using Make Commands

```bash
make coverage          # Terminal coverage report
make coverage-html     # HTML coverage report
make coverage-report   # Full analysis with XML + HTML
```

## Coverage Reports

### Terminal Report

Shows coverage percentage and missing lines directly in the terminal.

### HTML Report

- **Location**: `htmlcov/index.html`
- **Open with**: `open htmlcov/index.html`
- **Features**:
  - Interactive file browser
  - Line-by-line coverage highlighting
  - Missing lines highlighted in red
  - Covered lines in green

### XML Report

- **Location**: `coverage.xml`
- **Usage**: CI/CD integration, SonarQube, etc.

## Coverage Configuration

### `.coveragerc`

```ini
[run]
source = app
omit =
    */tests/*
    */test_*
    */__pycache__/*

[report]
show_missing = True
precision = 2

[html]
directory = htmlcov
```

### Current Coverage: **93.88%**

| Module                     | Coverage | Missing Lines      |
| -------------------------- | -------- | ------------------ |
| `app/handlers/item.py`     | 100.00%  | -                  |
| `app/api/schemas.py`       | 100.00%  | -                  |
| `app/api/server.py`        | 100.00%  | -                  |
| `app/domain/errors.py`     | 100.00%  | -                  |
| `app/infra/memory_repo.py` | 100.00%  | -                  |
| `app/api/routes/item.py`   | 91.30%   | 32-33, 50-51       |
| `app/domain/models.py`     | 88.24%   | 27, 29             |
| `app/api/di.py`            | 84.85%   | 49, 55, 61, 67, 73 |
| `app/tools/validator.py`   | 66.67%   | 11                 |

## Test Types

### Unit Tests (`tests/test_handlers.py`)

- Test business logic handlers
- Test domain models
- Test repository operations

### Integration Tests (`tests/test_api_items.py`)

- Test complete API endpoints
- Test request/response flow
- Test error handling
- Test partial updates

## Coverage Goals

- **Minimum**: 90% (enforced by `--cov-fail-under=90`)
- **Current**: 93.88%
- **Target**: 95%+

## Improving Coverage

To improve coverage, focus on:

1. **Error handling paths** in `app/tools/validator.py`
2. **Edge cases** in domain models validation
3. **Unused dependency injection functions** in `app/api/di.py`
4. **Exception handling** in API routes

## CI/CD Integration

```yaml
# Example GitHub Actions
- name: Run tests with coverage
  run: |
    export PYTHONPATH=.
    uv run pytest --cov=app --cov-report=xml --cov-fail-under=90

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```
