# Repository Guidelines

## Project Scope and Architecture

SkyBook is a Web Engineering course project: a simple airline ticket reservation
system built with Python 3.12, Django, and SQLite. Exercise 5 replaces the earlier
Flask scaffold with Django; keep the application Django-based and do not introduce
another web framework.

The Django project package belongs in `skybook/`, the main application in
`reservations/`, tests in `tests/`, and the management entry point is `manage.py`.
Configuration lives in `pyproject.toml`; CI runs from
`.github/workflows/ci.yml`. Before meaningful implementation, read the relevant
documents under `openspec/` and follow their requirements. Repository-local skills
support exploring, proposing, applying, updating, syncing, and archiving OpenSpec
changes. Exercise 5 permits the initial Django project, database schema, admin
registration, migrations, and model tests. Flight-search pages, authentication
screens, payments, the seat-map interface, and the complete booking workflow remain
out of scope.

## Domain Model and Booking Rules

The domain entities are `City`, `Airline`, `Flight`, `Seat`, and `Booking`; use
Django's built-in authentication user model rather than defining a custom `User`.
Support both guest and registered-user bookings by allowing `Booking.user` to be
null. Treat seat availability as a server-side invariant: database constraints must
prevent two bookings for the same flight seat, even with stale or concurrent
requests. Never rely only on browser validation or a future seat-map UI.

## Setup, Development, and Quality Commands

Use `uv` for environments and dependency management:

- `uv sync --all-extras --dev` installs Django, Ruff, Pytest, and coverage tooling.
- `uv run python manage.py runserver` starts the local Django server.
- `uv run python manage.py migrate` applies migrations.
- `uv run python manage.py makemigrations --check` detects model/migration drift.
- `uv run python manage.py check` runs Django's system checks.
- `uv run ruff format .` formats code; `uv run ruff format --check .` verifies it.
- `uv run ruff check .` lints code and checks imports; add `--fix` for safe fixes.
- `uv run pytest` runs Pytest with the configured application coverage report and
  missing-line output.

## Code Style and Testing

Follow Ruff settings in `pyproject.toml`: four-space indentation, double quotes,
100-character lines, and Python 3.12 syntax. Use `snake_case` for functions,
modules, and variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for
constants. Keep routes thin and place reusable logic in focused modules.

Name tests `test_<feature>.py` and functions `test_<behavior>()`. Use Django's test
utilities and database-aware Pytest markers where appropriate. New behavior and bug
fixes require tests, especially guest/registered booking paths, model constraints,
migrations, and duplicate-seat rejection. Do not reduce coverage.

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
