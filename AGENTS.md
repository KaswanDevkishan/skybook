# Repository Guidelines

## Project Scope and Architecture

SkyBook is a Web Engineering course project: a simple airline ticket reservation
system built with Python 3.12, Django, and SQLite. Exercise 5 replaces the earlier
Flask scaffold with Django; keep the application Django-based and do not introduce
another web framework. Exercise 8 adds proper Django forms for validated flight
search and simple guest-booking creation. Exercise 9 improves the existing interface
with semantic HTML, namespaced external CSS, responsive layout, and accessibility.
Exercise 10 adds one server-driven HTMX interaction that updates flight-search results
without reloading the complete page. Exercise 11 prepares the application for a Render
Web Service using Gunicorn, Render PostgreSQL, WhiteNoise, and environment-based
production configuration while preserving SQLite development.
The first major booking redesign adds classified and priced seats, enriched flight
results, flight-scoped seat selection, passenger details, authoritative JPY review,
atomic guest confirmation, and a booking receipt.

The Django project package belongs in `skybook/`, the main application in
`reservations/`, tests in `tests/`, and the management entry point is `manage.py`.
Configuration lives in `pyproject.toml`; CI runs from
`.github/workflows/ci.yml`. Before meaningful implementation, read the relevant
documents under `openspec/` and follow their requirements. Repository-local skills
support exploring, proposing, applying, updating, syncing, and archiving OpenSpec
changes. Exercise 11 permits the existing Django foundation, database schema, admin
registration, migrations, tests, basic views, GET flight search, CSRF-protected POST
guest booking for an existing seat, and focused semantic, responsive, and accessible
interface work. It also permits one pinned, progressively enhanced HTMX GET interaction,
a reusable flight-results partial, header-selected partial responses, accessible
loading feedback, and focused tests and documentation. Exercise 11 additionally permits
Gunicorn, a Python 3.12 PostgreSQL driver, database-URL parsing, WhiteNoise static
delivery, Render Blueprint configuration, secure proxy and cookie settings, production
settings tests, and deployment documentation. Preserve ordinary full-page and HTMX
search, the connected booking flow, migrations, health checks, and duplicate-seat
behavior. Authentication screens, real payments, aircraft-shaped SVG seat maps,
booking dashboards, cancellation, guest lookup, round trips, external airline APIs,
unrelated UI changes, other client-side frameworks, Docker unless genuinely required,
Redis, Celery, workers, and file uploads remain out of scope.

## Domain Model and Booking Rules

The domain entities are `City`, `Airline`, `Flight`, `Seat`, and `Booking`; use
Django's built-in authentication user model rather than defining a custom `User`.
Support both guest and registered-user bookings by allowing `Booking.user` to be
null. Treat seat availability as a server-side invariant: database constraints must
prevent two bookings for the same flight seat, even with stale or concurrent
requests. Never rely only on browser validation or a future seat-map UI.
Seats use Economy/Business and Window/Middle/Aisle choices with whole-yen Decimal
prices. Confirmed bookings store immutable base fare, taxes and fees, total, reference,
and creation time. Calculate the current 10% fee authoritatively on the server and
round half-up to whole yen.

## Setup, Development, and Quality Commands

Use `uv` for environments and dependency management:

- `uv sync --all-extras --dev` installs Django, Ruff, Pytest, and coverage tooling.
- `uv run python manage.py runserver` starts the local Django server.
- `uv run python manage.py migrate` applies migrations.
- `uv run python manage.py makemigrations --check` detects model/migration drift.
- `uv run python manage.py check` runs Django's system checks.
- Production-like `uv run python manage.py check --deploy` checks secure settings.
- `uv run python manage.py collectstatic --noinput` verifies static collection.
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
migrations, search validation, CSRF protection, retained form values, and
duplicate-seat rejection. Interface changes also require tests for static assets,
semantic landmarks, skip navigation, visible labels, and accessible error markup. Do
not reduce coverage. Exercise 10 tests must distinguish complete-page and HTMX partial
responses, cover strict `HX-Request` detection, filtering, validation, empty states,
the HTMX form attributes, loading and live-region semantics, progressive enhancement,
and migration safety. Exercise 11 tests must cover safe environment defaults and
overrides, required Render secrets, SQLite and PostgreSQL selection, WhiteNoise
middleware order and manifest storage, proxy HTTPS and secure cookies, Render
build/start/migration configuration, the health-check path, static collection, and
Gunicorn WSGI import.

## Commits and Pull Requests

Use short, imperative commit subjects consistent with history, such as
`Create test_app.py`. Keep commits focused. Pull requests should summarize the
change, reference the relevant issue or OpenSpec document, list verification
commands, and include screenshots for UI changes. CI must pass.

## Security and Repository Hygiene

Never commit tokens, passwords, secrets, `.env` files, virtual environments
(`.venv/`), caches (`__pycache__/`, `.pytest_cache/`, `.ruff_cache/`), or local
SQLite/database files. Never commit `SECRET_KEY`, `DATABASE_URL`, Render credentials,
or collected static output. Ignore rules are only a safety net. Load production
secrets from the environment, keep `DEBUG` false on Render, and do not weaken host,
CSRF, cookie, or HTTPS protections to pass deployment. The current development secret
is not suitable for deployment. Render's app-local filesystem is ephemeral; future
uploaded media must use persistent object storage.
