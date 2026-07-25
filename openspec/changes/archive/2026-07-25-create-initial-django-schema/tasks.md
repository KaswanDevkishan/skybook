## 1. Confirm the Course-Phase Gate

- [x] 1.1 Confirm that Exercise 4 has ended and obtain approval to replace the
  Flask-only architecture and application-feature prohibition; do not continue with
  implementation before this gate is satisfied.
- [x] 1.2 Review GitHub issues #2, #3, and #4 and reconcile any additional acceptance
  criteria with the proposal, design, and specs before changing application code.

## 2. Generate the Django Foundation

- [x] 2.1 Update `pyproject.toml` to replace Flask with Django, add the minimal
  Django-aware test tooling, and configure Pytest and coverage for the new packages.
- [x] 2.2 Use `django-admin startproject skybook .` to generate the project and verify
  its settings use SQLite for development.
- [x] 2.3 Use `manage.py startapp reservations`, install the application in Django
  settings, and retain the generated structure needed by Django.
- [x] 2.4 Remove obsolete Flask application files, Flask smoke tests, `wsgi.py`, and
  dependency references without removing unrelated user files.

## 3. Implement the Reservation Schema

- [x] 3.1 Implement `City` and `Airline` with names, unique normalized codes, and
  tested human-readable string representations.
- [x] 3.2 Implement `Flight` relationships, schedule fields, display text, distinct-city
  and increasing-time checks, and scheduled-identity uniqueness.
- [x] 3.3 Implement flight-owned `Seat` records with display text and per-flight seat
  number uniqueness.
- [x] 3.4 Implement `Booking` with a unique seat reference, nullable
  `settings.AUTH_USER_MODEL` reference, guest contact fields, deletion behavior, and
  useful display text.
- [x] 3.5 Register `City`, `Airline`, `Flight`, `Seat`, and `Booking` in Django admin.

## 4. Create and Verify Database Migrations

- [x] 4.1 Generate and review the initial `reservations` migration so its fields,
  relationships, deletion rules, checks, and uniqueness constraints match the specs.
- [x] 4.2 Apply all migrations to a clean disposable SQLite database and verify Django
  reports no unapplied migrations or model changes.
- [x] 4.3 Confirm the local SQLite database remains ignored and is not added to version
  control.

## 5. Test Model Behavior

- [x] 5.1 Add model tests for valid relationships and every model's `__str__`
  representation.
- [x] 5.2 Add database-level tests for duplicate city and airline codes, invalid flight
  routes and times, duplicate scheduled flights, and duplicate seats per flight.
- [x] 5.3 Add tests for registered bookings, null-user guest bookings, user deletion,
  and database rejection of a second booking for the same seat.
- [x] 5.4 Verify the tests do not introduce flight-search, seat-map, authentication,
  payment, or complete booking workflow behavior.

## 6. Update Guidance and Documentation

- [x] 6.1 Update `README.md` with the generated Django layout, `uv` setup, development
  server, migration, admin, test, lint, and format commands plus the deferred-feature
  boundary.
- [x] 6.2 Update `AGENTS.md` for the approved Django architecture, model invariants,
  commands, test expectations, security rules, and post-Exercise-4 scope.
- [x] 6.3 Update `openspec/config.yaml` and the main repository guidance specification
  so current framework, implemented schema behavior, and deferred features are
  unambiguous.
- [x] 6.4 Search documentation, CI, configuration, and source files for stale Flask
  commands, paths, dependencies, or claims and resolve them within this change.

## 7. Final Verification

- [x] 7.1 Run `uv sync --all-extras --dev`, the Django system check, migration drift
  check, and clean-database migration application.
- [x] 7.2 Run `uv run ruff format --check .`, `uv run ruff check .`, and
  `uv run pytest`, confirming configured coverage does not decrease.
- [x] 7.3 Run strict OpenSpec validation for `create-initial-django-schema` and inspect
  the final diff for scope, generated artifacts, ignored local state, and accidental
  secrets.
