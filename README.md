# SkyBook: Airline Ticket Reservation System

SkyBook is a web application for searching and booking flights between a
predefined set of cities. Users search by route, date, and class; pick a
flight; select a seat from an interactive seat map; and confirm a booking.
The system prevents double-booking and supports both guest and registered
bookings.

This project is developed for the Web Engineering course
(Exercise 1–3 build-up: proposal → data model/UI/architecture → dev
environment setup).

## Project Structure
skybook/
├── app/                # Flask application package
│   ├── init.py         # App factory, routes
│   ├── models/         # (planned) SQLAlchemy models: City, Airline, Flight, Seat, User, Booking
│   ├── routes/         # (planned) Blueprints: search, booking, auth
│   └── templates/      # (planned) Jinja2 HTML templates
├── tests/              # Pytest test suite
│   └── test_app.py
├── wsgi.py             # Development server entry point
├── pyproject.toml      # Project metadata + tool configuration
├── uv.lock             # Locked dependency versions
├── .gitignore
└── README.md

## Data Model (summary)

| Entity  | Key columns                                              |
|---------|-----------------------------------------------------------|
| City    | id, name                                                   |
| Airline | id, name                                                    |
| Flight  | id, airline_id, origin_city_id, dest_city_id, departure_time |
| Seat    | id, flight_id, row, column, class, is_booked                |
| User    | id, username, password_hash, display_name                   |
| Booking | id, user_id (nullable), seat_id, passenger_name, booking_date, status |

Full details and the booking user flow are documented in the Exercise 1 and
Exercise 2 project proposal PDFs.

## Environment & Tooling

| Purpose            | Tool                              |
|---------------------|-----------------------------------|
| Language / runtime  | Python 3.12                       |
| Package/env manager | [uv](https://docs.astral.sh/uv/)  |
| Web framework       | Flask 3                           |
| Database (dev)      | SQLite                            |
| Formatting & linting| Ruff                               |
| Testing             | Pytest                             |
| Coverage            | pytest-cov / coverage.py           |

Tool configuration lives in `pyproject.toml` under `[tool.ruff]`,
`[tool.pytest.ini_options]`, and `[tool.coverage.*]`.

## Getting Started

### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- Python 3.12 (uv will fetch it automatically if not present)

### Setup

```bash
git clone <repo-url>
cd skybook
uv sync              # creates .venv and installs all dependencies (incl. dev tools)
```

### Run the app

```bash
uv run python wsgi.py
```

Visit `http://127.0.0.1:5000` — you should see `SkyBook is running.`
A `/health` endpoint is also available for a quick status check.

### Formatting & linting

```bash
uv run ruff format .     # auto-format code
uv run ruff format --check .   # check formatting without changing files
uv run ruff check .       # lint
uv run ruff check --fix . # lint and auto-fix what's safe to fix
```

### Tests & coverage

```bash
uv run pytest
```

`pytest` is configured (via `addopts` in `pyproject.toml`) to always run
with coverage and print a missing-lines report for the `app/` package.

## Status

This exercise (Exercise 3) sets up the development environment only:
Git repository, uv-managed virtual environment, Ruff (format + lint),
Pytest + coverage, `.gitignore`, and this README. Application features
(database models, routes, seat map UI) are implemented in later
exercises, following the design in the Exercise 1/2 proposal.










