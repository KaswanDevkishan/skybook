````markdown
# SkyBook: Airline Ticket Reservation System

SkyBook is a web application for searching and booking flights between a predefined set of cities. Users search by route, date, and class; pick a flight; select a seat from an interactive seat map; and confirm a booking. The system prevents double-booking and supports both guest and registered bookings.

This project is developed for the Web Engineering course through Exercises 1–4:

- Exercise 1: Project proposal
- Exercise 2: Data model, user flow, and architecture
- Exercise 3: Development environment setup
- Exercise 4: AI tools setup

## Project Structure

```text
skybook/
├── app/                # Flask application package
│   ├── __init__.py     # Application factory and basic routes
│   ├── models/         # Planned SQLAlchemy models
│   ├── routes/         # Planned blueprints: search, booking, authentication
│   ├── templates/      # Planned Jinja2 templates
│   └── static/         # Planned CSS and JavaScript files
├── tests/              # Pytest test suite
│   └── test_app.py
├── wsgi.py             # Development server entry point
├── pyproject.toml      # Project metadata and tool configuration
├── uv.lock             # Locked dependency versions
├── AGENTS.md           # Coding-agent instructions
├── .codex/             # Codex-compatible OpenSpec skills
├── openspec/           # OpenSpec configuration and specifications
├── .gitignore
└── README.md
````

## Data Model Summary

| Entity  | Key columns                                                           |
| ------- | --------------------------------------------------------------------- |
| City    | id, name                                                              |
| Airline | id, name                                                              |
| Flight  | id, airline_id, origin_city_id, dest_city_id, departure_time          |
| Seat    | id, flight_id, row, column, class, is_booked                          |
| User    | id, username, password_hash, display_name                             |
| Booking | id, user_id (nullable), seat_id, passenger_name, booking_date, status |

Full details and the booking user flow are documented in the Exercise 1 and Exercise 2 project proposal PDFs.

## Environment and Tooling

| Purpose                         | Tool                     |
| ------------------------------- | ------------------------ |
| Language and runtime            | Python 3.12              |
| Package and environment manager | uv                       |
| Web framework                   | Flask 3                  |
| Development database            | SQLite                   |
| Formatting and linting          | Ruff                     |
| Testing                         | Pytest                   |
| Coverage                        | pytest-cov / coverage.py |
| Coding agent                    | OpenAI Codex             |
| Specification workflow          | OpenSpec                 |
| Version control                 | Git and GitHub           |

Tool configuration lives in `pyproject.toml` under `[tool.ruff]`, `[tool.pytest.ini_options]`, and `[tool.coverage.*]`.

## Getting Started

### Prerequisites

* uv installed
* Python 3.12

### Setup

```bash
git clone <repo-url>
cd skybook
uv sync
```

The `uv sync` command creates the local `.venv` and installs the project dependencies and development tools.

### Run the Application

```bash
uv run python wsgi.py
```

Visit:

```text
http://127.0.0.1:5000
```

A `/health` endpoint is also available for checking the application status.

### Formatting and Linting

```bash
uv run ruff format .
uv run ruff format --check .
uv run ruff check .
uv run ruff check --fix .
```

### Tests and Coverage

```bash
uv run pytest
```

Pytest is configured through `pyproject.toml` to run with coverage and print a missing-lines report for the `app/` package.

## AI-Assisted Development

SkyBook is configured for AI-assisted development using OpenAI Codex and OpenSpec.

### Coding Agent

Codex is used for:

* Repository analysis
* Project planning
* Implementation assistance
* Code review
* OpenSpec workflows

Project-specific instructions for the coding agent are stored in:

```text
AGENTS.md
```

Start Codex from the project root:

```bash
codex
```

### Agent Skills

OpenSpec installed six Codex-compatible skills for:

* Exploring a proposed change
* Creating a proposal
* Applying a change
* Updating an active change
* Synchronizing specifications
* Archiving completed changes

The skills are stored in:

```text
.codex/skills/
```

SkyBook remains a Flask project. Django-oriented guidance must not be used to convert the application to Django.

### OpenSpec

OpenSpec is used for specification-driven development. Meaningful project changes should be proposed and reviewed before implementation.

OpenSpec configuration and project specifications are stored in:

```text
openspec/
```

The initial OpenSpec task reviewed and refined the project’s AI-assisted development setup.

The task checked:

* `AGENTS.md`
* `README.md`
* `pyproject.toml`
* `.gitignore`
* OpenSpec configuration
* Installed skills
* Formatting commands
* Linting commands
* Testing commands
* Repository structure
* Flask-specific instructions

The task did not implement application features such as:

* Database models
* Flight search
* Seat selection
* Booking
* Authentication
* Seat-map interface

The completed change was archived under the OpenSpec changes archive.

### Human Review and Verification

AI-generated changes must be reviewed before they are committed.

After AI-assisted changes, run:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

Review repository changes with:

```bash
git status
git diff
```

The following files must not be committed:

* Tokens
* Passwords
* API keys
* `.env` files
* Virtual environments
* Cache files
* Coverage output
* Local SQLite databases

## Current Status

Exercises 1–4 have established:

* The project topic and proposal
* The basic data model
* The main user flow
* The architecture sketch
* The Flask development environment
* Git and GitHub integration
* uv dependency management
* Ruff formatting and linting
* Pytest and coverage
* Codex coding-agent setup
* `AGENTS.md`
* OpenSpec configuration
* OpenSpec skills
* A completed and archived OpenSpec setup-review task

Application features such as database models, flight search, seat selection, booking, authentication, and the seat-map interface will be implemented in later exercises.

```
```
