# AGENTS.md

## Build/Lint/Test Commands
- **Install dependencies**: `pip install -r requirements.txt`
- **Run all tests**: `PYTHONPATH=. pytest -q`
- **Run single test**: `PYTHONPATH=. pytest tests/test_feed.py::test_is_stable_title -q`
- **Lint code**: `flake8 app tests` (currently commented out in CI)

## Code Style Guidelines
- **Python version**: 3.11
- **Import style**: Standard library imports first, then third-party, then local imports
- **Formatting**: Follow PEP 8, use flake8 for linting
- **Type hints**: Use type hints for function parameters and return values
- **Naming**: snake_case for variables/functions, UPPER_CASE for constants
- **Error handling**: Use specific exceptions, log warnings for retries, raise RuntimeError after retries exhausted
- **Logging**: Use module-level logger, format: `"%(asctime)s %(levelname)s %(message)s"`
- **Testing**: Use pytest, write simple unit tests with descriptive function names
- **Structure**: Separate concerns into modules (feed, state, notifier, web)