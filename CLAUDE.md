# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```bash
pip install -e ".[test]"
```

**Run tests (unit only, excludes integration/spark):**
```bash
pytest
```

**Run a single test:**
```bash
pytest tests/test_methods.py::test_hello
```

**Run integration tests:**
```bash
pytest -m integration
```

**Lint:**
```bash
pylint src/
flake8 src/
```

**Format:**
```bash
black src/ tests/
```

**Type check:**
```bash
pyright
```

**Security scan:**
```bash
bandit -r src/
```

**Pre-commit hooks:**
```bash
pre-commit run --all-files
```

**Build package:**
```bash
flit build
```

## Architecture

This is a Python package template using **Flit** for building/publishing (configured in `pyproject.toml` via `[tool.flit.module]`). Source lives under `src/python_package/` with the package version defined in `src/python_package/__init__.py`.

**Test markers** (defined in `pyproject.toml`): Tests are categorized as `unit`, `integration`, `spark`, `gpu`, `notebooks`, or `slow`. The default `pytest` run excludes `integration` tests. Tests with `_int_` in their node ID are automatically marked as `integration`; tests with `spark` in their node ID are automatically marked as `spark` (see `tests/conftest.py`).

**Code style**: max line length is 120 (Black, flake8, pylint all configured to this). isort prepends `from __future__ import annotations` to all files automatically via pre-commit.

**Coverage**: configured with `branch = true`; CI requires 100% coverage (`fail_under = 100`), though the pytest default opts out (`--cov-fail-under 0`).
