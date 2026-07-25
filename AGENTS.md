# Repository Guidelines

## Project Scope and Architecture

SkyBook is a Web Engineering course project: a simple airline ticket reservation
system built with Python 3.12, Flask 3, and SQLite. Keep the application Flask-based;
do not convert it to Django or introduce another web framework.

Application code belongs in `app/`, tests in `tests/`, and the entry point is
`wsgi.py`. Configuration lives in `pyproject.toml`; CI runs from
`.github/workflows/ci.yml`. Before meaningful implementation, read the relevant
documents under `openspec/` and follow their requirements. Repository-local skills
support exploring, proposing, applying, updating, syncing, and archiving OpenSpec
changes. During Exercise 4, do not implement application features; limit work to
the documentation, agent guidance, and configuration explicitly required.

## Domain Model and Booking Rules

The planned entities are `City`, `Airline`, `Flight`, `Seat`, `User`, and `Booking`.
Support both guest and registered-user bookings. Treat seat availability as a
server-side invariant: future booking logic must prevent two bookings for the same
flight seat, even with stale or concurrent requests. Never rely only on browser
validation or the seat-map UI.

## Setup, Development, and Quality Commands

Use `uv` for environments and dependency management:

- `uv sync --all-extras --dev` installs Flask, Ruff, Pytest, and coverage tooling.
- `uv run python wsgi.py` starts the local Flask server.
- `uv run ruff format .` formats code; `uv run ruff format --check .` verifies it.
- `uv run ruff check .` lints code and checks imports; add `--fix` for safe fixes.
- `uv run pytest` runs Pytest with the configured `app/` coverage report and
  missing-line output.

## Code Style and Testing

Follow Ruff settings in `pyproject.toml`: four-space indentation, double quotes,
100-character lines, and Python 3.12 syntax. Use `snake_case` for functions,
modules, and variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for
constants. Keep routes thin and place reusable logic in focused modules.

Name tests `test_<feature>.py` and functions `test_<behavior>()`. Use Flask's test
client. New behavior and bug fixes require tests, especially
guest/registered booking paths and duplicate-seat rejection. Do not reduce coverage.

## Commits and Pull Requests

Use short, imperative commit subjects consistent with history, such as
`Create test_app.py`. Keep commits focused. Pull requests should summarize the
change, reference the relevant issue or OpenSpec document, list verification
commands, and include screenshots for UI changes. CI must pass.

## Security and Repository Hygiene

Never commit tokens, passwords, secrets, `.env` files, virtual environments
(`.venv/`), caches (`__pycache__/`, `.pytest_cache/`, `.ruff_cache/`), or local
SQLite/database files. Ignore rules are only a safety net. Load production secrets
from the environment; the current development secret is not suitable for deployment.
