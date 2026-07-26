## 1. Seed Catalog and Validation

- [x] 1.1 Expand the destination catalog to approximately 30–40 stable, uniquely
  coded major Japanese airport or airport-served destinations while retaining every
  legacy code/name pair
- [x] 1.2 Define a curated set of stable flight identities and valid schedules covering
  Hokkaido, Tohoku, Kanto, Chubu, Kansai, Chugoku, Shikoku, Kyushu, and Okinawa
- [x] 1.3 Add atomic preflight validation for duplicate destination and flight
  identities, unknown endpoints, same-origin routes, and non-positive durations

## 2. Preservation-Safe Seeding

- [x] 2.1 Keep destination creation keyed by stable code without renaming, replacing,
  deleting, or changing identifiers or relationships of existing `City` rows
- [x] 2.2 Create schedule datetimes only in missing-flight defaults so existing flight
  endpoints, departure times, and arrival times never change on later runs
- [x] 2.3 Create missing Economy and Business seats with the established types and
  whole-yen JPY prices without duplicating or mutating existing seats
- [x] 2.4 Confirm the command never writes `Booking` records and retains the existing
  database-backed duplicate-seat invariant

## 3. Homepage and Shared Layout

- [x] 3.1 Replace the homepage eyebrow, heading, and description with the exact supplied
  Japan-focused copy while retaining the flight-search action
- [x] 3.2 Remove the shared site footer markup and delete only footer-specific unused
  stylesheet rules
- [x] 3.3 Preserve the SkyBook homepage brand link, Flights current navigation state,
  skip link, semantic landmarks, responsive behavior, and visible focus treatment
  without adding Sign In or Create Account links

## 4. Automated Coverage

- [x] 4.1 Test the approximate destination count, stable unique codes, clear names,
  requested regional coverage, and valid origin/destination relationships
- [x] 4.2 Test first-run future schedules and repeated seeding without destination,
  airline, flight, or seat duplication
- [x] 4.3 Snapshot and test preservation of existing city identifiers and fields,
  flight endpoints and schedules, seat identities and prices, unrelated records, and
  every booking field across a later-date repeated run
- [x] 4.4 Test that every newly seeded flight has non-duplicated Economy and Business
  seats, Window/Middle/Aisle types, and positive whole-yen JPY pricing
- [x] 4.5 Update view and static-asset tests for the exact hero copy, complete footer
  absence, removed footer-only styles, compact navigation, and retained accessibility
- [x] 4.6 Retain or extend regression coverage for full-page and HTMX flight search and
  the connected flight-specific booking, pricing, confirmation, and receipt flow

## 5. Documentation and Planning Consistency

- [x] 5.1 Update README destination, seeding, interface, search, booking, and Render
  guidance to describe representative major domestic Japanese airport data that is
  neither complete nor a live aviation schedule
- [x] 5.2 Reconcile active OpenSpec artifacts and repository guidance with the final
  implementation, preservation guarantees, footer removal, deferred authentication,
  and related issues `#<destination-issue>` and `#<homepage-issue>`

## 6. Verification

- [x] 6.1 Run `uv run ruff format .`
- [x] 6.2 Run `uv run ruff check .`
- [x] 6.3 Run `uv run pytest`
- [x] 6.4 Run `uv run python manage.py check`
- [x] 6.5 Run `uv run python manage.py makemigrations --check --dry-run`
- [x] 6.6 Run strict OpenSpec validation for the change
- [x] 6.7 Run `git diff --check` and confirm no commit, push, or archive was performed
