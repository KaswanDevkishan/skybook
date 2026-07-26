# SkyBook

SkyBook is a simple airline ticket reservation system for a Web Engineering course.
Exercise 8 adds validated Django forms for flight search and simple guest booking to
the existing Django application and database schema. SQLite is used for local
development.

The current milestone provides:

- A generated Django project and `reservations` application
- `City`, `Airline`, `Flight`, `Seat`, and `Booking` models
- Django's built-in authentication user model for registered bookings
- Guest bookings through a nullable `Booking.user`
- Database constraints for valid routes, times, scheduled flights, seats, and bookings
- Django admin registration, migrations, model tests, and coverage
- Basic home, searchable flight-list, flight-detail, guest-booking, and health views
- GET-based flight search with validated city and departure-date input
- CSRF-protected guest booking with validated seat, passenger name, and email input

Authentication screens, payments, the interactive seat-map interface, external
airline APIs, production styling, and the complete booking workflow are intentionally
deferred. Search by seat class is also omitted because the current models do not
contain a compatible seat-class field.

## Project Structure

```text
skybook/
├── manage.py
├── skybook/                  # Django project settings, URLs, ASGI, and WSGI
├── reservations/             # Main domain application
│   ├── migrations/
│   ├── templates/reservations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── tests/                    # Pytest model, constraint, URL, and view tests
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

## Public HTTP Endpoints

All application routes use the `reservations` URL namespace.

| Name | Method and URL | Arguments or fields | Response |
| --- | --- | --- | --- |
| `reservations:home` | `GET /` | None | Renders the home page with links to the flight list and booking form; status 200 |
| `reservations:flight_list` | `GET /flights/` | Query fields `origin`, `destination`, and `departure_date` | With no query, renders all flights ordered by ascending departure time. A valid query filters exact cities and departure date in that order. Invalid input re-renders the bound form with visible errors, retained values, and no partially filtered results; status 200 |
| `reservations:flight_detail` | `GET /flights/<int:flight_id>/` | `flight_id`: database ID of a flight | Renders the airline, route, departure time, and arrival time; status 200, or 404 when the flight does not exist |
| `reservations:booking_new` | `GET /booking/new/` | None | Renders an unbound, CSRF-protected booking form; status 200 |
| `reservations:booking_submit` | `POST /booking/submit/` | Form fields `seat`, `passenger_name`, and `passenger_email` | Creates a guest booking and redirects to `/` with status 302 when valid. Invalid or duplicate-seat input re-renders the bound form with visible errors and retained values without creating a booking; status 200. Missing CSRF returns 403, and unsupported methods return 405 |
| `reservations:health` | `GET /health/` | None | Returns a non-empty plain-text health response; status 200 |

The flight-search form requires all three fields, resolves origin and destination to
existing cities, rejects a route whose cities are the same, and validates the date
before filtering.

The booking form requires all three fields, uses Django email validation, resolves the
seat to an existing record, and rejects a seat that is already booked. Successful
submissions create a guest `Booking` by mapping `passenger_name` and `passenger_email`
to `guest_name` and `guest_email`; `Booking.user` remains null. Form validation
improves error reporting, while the existing database uniqueness constraint remains
the final protection against stale or concurrent duplicate-seat requests.

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

Visit `http://127.0.0.1:8000/` for the home page or
`http://127.0.0.1:8000/admin/` to use Django admin after creating a local superuser:

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
foundation and schema are defined by the archived `create-initial-django-schema`
change, and the basic HTTP views by `add-basic-django-views`. Exercise 8 form handling
is defined by `implement-django-forms` and relates to
[issue #11](https://github.com/KaswanDevkishan/skybook/issues/11),
[issue #12](https://github.com/KaswanDevkishan/skybook/issues/12), and
[issue #13](https://github.com/KaswanDevkishan/skybook/issues/13).

AI-assisted changes require human review before commit. Inspect the final state with:

```bash
git status
git diff
```

Do not commit tokens, passwords, API keys, `.env` files, virtual environments, caches,
coverage output, or local database files. Production secrets must be supplied through
the environment; the checked-in fallback secret is development-only.
