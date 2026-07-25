# SkyBook

SkyBook is a simple airline ticket reservation system for a Web Engineering course.
Exercise 5 establishes a runnable Django application and its initial database schema.
SQLite is used for local development.

The current milestone provides:

- A generated Django project and `reservations` application
- `City`, `Airline`, `Flight`, `Seat`, and `Booking` models
- Django's built-in authentication user model for registered bookings
- Guest bookings through a nullable `Booking.user`
- Database constraints for valid routes, times, scheduled flights, seats, and bookings
- Django admin registration, migrations, model tests, and coverage

Flight-search pages, authentication screens, payments, the seat-map interface, and the
complete booking workflow are intentionally deferred.

## Project Structure

```text
skybook/
├── manage.py
├── skybook/                  # Django project settings, URLs, ASGI, and WSGI
├── reservations/             # Main domain application
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   └── models.py
├── tests/                    # Pytest model and constraint tests
├── openspec/                 # Specifications and active changes
├── pyproject.toml            # Dependencies and quality-tool configuration
├── uv.lock                   # Locked dependency versions
├── AGENTS.md                 # Repository guidance for coding agents
└── .github/workflows/ci.yml
```

## Data Model

| Model | Purpose and relationships |
| --- | --- |
| `City` | Named location with a unique normalized code |
| `Airline` | Named carrier with a unique normalized code |
| `Flight` | Airline service between distinct cities with increasing departure and arrival times |
| `Seat` | Seat number unique within a flight |
| `Booking` | Unique reservation for a seat, linked to either a Django user or guest contact data |

The database prevents two bookings from referencing the same seat. This invariant does
not depend on browser validation or a future seat-map interface.

## Setup

Prerequisites:

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

Install runtime and development dependencies:

```bash
uv sync --all-extras --dev
```

Apply migrations:

```bash
uv run python manage.py migrate
```

Start the development server:

```bash
uv run python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` to use Django admin after creating a local
superuser:

```bash
uv run python manage.py createsuperuser
```

Local SQLite databases are ignored by Git and must not be committed.

## Verification

Run Django system and migration checks:

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

Format and lint:

```bash
uv run ruff format .
uv run ruff format --check .
uv run ruff check .
```

Run tests with the configured coverage report:

```bash
uv run pytest
```

CI runs dependency installation, Ruff formatting and lint checks, and Pytest.

## OpenSpec and Review

Meaningful changes follow the specifications under `openspec/`. The Exercise 5 Django
foundation and schema are defined by the `create-initial-django-schema` change, which
relates to GitHub issues #2, #3, and #4.

AI-assisted changes require human review before commit. Inspect the final state with:

```bash
git status
git diff
```

Do not commit tokens, passwords, API keys, `.env` files, virtual environments, caches,
coverage output, or local database files. Production secrets must be supplied through
the environment; the checked-in fallback secret is development-only.
