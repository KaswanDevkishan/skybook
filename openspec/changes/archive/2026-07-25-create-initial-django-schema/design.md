## Context

The repository currently contains a minimal Flask application factory, `wsgi.py`,
Flask smoke tests, and Flask-oriented documentation. The current OpenSpec context
also fixes the project to Flask and limits Exercise 4 to documentation and
configuration, so this design is conditional: it MUST NOT be applied until the course
has moved beyond Exercise 4 and the `repository-agent-guidance` delta is approved.

Once approved, this is an intentionally small framework replacement for a Web
Engineering course. It establishes a Django project, one domain application, an
SQLite schema, admin access, and model tests. It does not create public product pages
or a booking service.

## Goals / Non-Goals

**Goals:**

- Produce a runnable Django project using the framework's standard generators.
- Represent cities, airlines, flights, seats, and guest or registered-user bookings
  with explicit relational integrity.
- Use Django's built-in authentication model instead of defining a duplicate user.
- Make the schema inspectable through Django admin and reproducible through committed
  migrations.
- Keep the existing `uv`, Ruff, Pytest, coverage, and SQLite development workflow.
- Update project guidance and OpenSpec context as part of the approved phase change.

**Non-Goals:**

- Applying any application or dependency change while Exercise 4 remains active.
- Preserving Flask or running Flask and Django side by side after the transition.
- Flight-search pages, seat maps, authentication pages, payment, or a complete
  booking workflow.
- Production deployment, production database selection, APIs, seed data, pricing, or
  advanced airline operations.
- Solving every future concurrency concern in application code; this change establishes
  the database uniqueness invariant on booked seats for later workflows to use.

## Decisions

1. **Use generated Django structure after the phase gate.** Run `django-admin
   startproject skybook .`, then `python manage.py startapp reservations`, and keep
   project configuration in `skybook/` and domain code in `reservations/`. Generators
   make the course project recognizable and satisfy the requested creation workflow.
   Manually assembling Django files was rejected because it obscures provenance;
   embedding Django in the existing Flask package was rejected because parallel
   frameworks add needless complexity.

2. **Perform a clean framework replacement.** Remove the Flask `app/` package,
   `wsgi.py`, Flask smoke tests, and Flask dependency after the Django scaffold exists.
   Retaining two entry points was rejected because the requested architecture is a
   replacement and dual-framework configuration would confuse students and CI.

3. **Use one `reservations` application.** All five domain models live in a single
   app for this course-sized system. Splitting flights and bookings into separate apps
   was rejected for now because the model graph is small and no independent lifecycle
   exists yet.

4. **Model stable identifiers and relationships explicitly.**

   - `City` has a unique short code and a name.
   - `Airline` has a unique short code and a name.
   - `Flight` belongs to an airline, references distinct origin and destination cities,
     records a flight number and timezone-aware departure/arrival values, requires
     arrival after departure, and prevents duplicate scheduled flight identities.
   - `Seat` belongs to a flight and has a seat number unique within that flight.
   - `Booking` references one seat with a database uniqueness constraint, optionally
     references `settings.AUTH_USER_MODEL`, and stores guest name and email fields that
     can identify a guest when `user` is null.

   Short codes and flight/seat labels remain strings so leading zeroes and airline
   conventions are preserved. A custom user model was rejected because the built-in
   authentication model is explicitly required. A bare nullable user without guest
   contact fields was rejected because it could not represent a useful guest booking.

5. **Put critical invariants in the database.** Use `UniqueConstraint` for a seat
   number per flight, a booking per seat, and the scheduled flight identity; use
   `CheckConstraint` for distinct cities and increasing flight times. Model validation
   remains helpful, but tests MUST exercise database rejection because future stale or
   concurrent requests cannot be secured by forms alone.

6. **Use protective deletion behavior for operational data.** City and airline
   references use `PROTECT`; flight-owned seats use `CASCADE`; a booked seat uses
   `PROTECT`; and `Booking.user` uses `SET_NULL` so deleting a user does not erase the
   booking. This keeps historical bookings while avoiding accidental removal of
   referenced schedule data. More elaborate archival policies are deferred.

7. **Use migrations as the schema source of truth.** Commit the generated initial
   migration and verify `makemigrations --check`, migration application on a clean
   SQLite database, and the model suite. The local database file remains ignored.
   Hand-written SQL was rejected because it would duplicate Django's schema state.

8. **Retain the repository quality interface.** Replace Flask with Django and add
   `pytest-django`, configuring the settings module and coverage target in
   `pyproject.toml`. CI continues to use `uv`, Ruff, and Pytest. Django's own test
   classes remain acceptable under Pytest, keeping tests idiomatic without adding a
   second test command as the primary workflow.

9. **Treat documentation changes as part of the architecture transition.** README,
   AGENTS, OpenSpec configuration, and the repository guidance specification change
   together only when the phase gate is approved. Until then, the existing Flask-only
   guidance remains authoritative.

## Risks / Trade-offs

- [The requested architecture contradicts current course governance] → Keep this
  change planning-only and require explicit post-Exercise-4 approval before apply.
- [Replacing Flask breaks existing imports and commands] → Make the replacement
  atomic, update docs and CI configuration in the same change, and search for stale
  Flask references.
- [SQLite differs from a production database] → Restrict the claim to development and
  rely on portable Django constraints where SQLite supports them.
- [Database constraints surface `IntegrityError` rather than friendly feedback] →
  Test the invariant now and add user-facing error handling in the later booking
  workflow.
- [A booking-per-seat constraint prevents rebooking after cancellation] → Do not add
  cancellation status in this initial schema; revise the invariant deliberately when
  lifecycle requirements exist.
- [Deleting users can leave guest-like booking rows] → Retain guest contact fields and
  use `SET_NULL`; later privacy requirements can define anonymization or retention.

## Migration Plan

1. Confirm that Exercise 4 has ended and approve the repository-guidance delta.
2. Update dependencies, generate the Django project and `reservations` app, then move
   settings into their final checked-in form.
3. Add models, admin registrations, test configuration, and the initial migration.
4. Apply migrations to a clean disposable SQLite database and run the full quality
   suite.
5. Remove obsolete Flask files and dependency references, update documentation and
   OpenSpec configuration, and verify no stale framework guidance remains.
6. If the transition must be rolled back before data is retained, revert the focused
   change and recreate the ignored development database. Migrating real persisted
   course data is outside this initial change.

## Open Questions

- Which course milestone formally authorizes replacing the Exercise 4 Flask-only
  constraint? Implementation remains blocked until that is confirmed.
- Do issues #2, #3, and #4 define exact model fields or naming beyond the requirements
  available in this request? Their acceptance criteria should be checked before apply.
