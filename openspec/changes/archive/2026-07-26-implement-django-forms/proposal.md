## Why

SkyBook's current flight list has no validated search input, and its placeholder booking
submission manually checks two strings without selecting a seat or creating a `Booking`.
Exercise 8 now permits a focused Django-forms workflow that safely accepts user input while
preserving the existing database-backed duplicate-seat invariant.

## What Changes

- Add `FlightSearchForm` with required origin, destination, and departure-date fields, submitted
  with GET and validated so origin and destination differ.
- Filter flights from validated search data and order results by departure time while retaining
  submitted values and displaying form errors.
- Replace placeholder booking input handling with a CSRF-protected Django form for `seat`,
  passenger name, and passenger email.
- Validate seat existence and availability, create guest `Booking` records using the existing
  `seat`, `guest_name`, and `guest_email` model fields, and redirect after success.
- Keep the existing schema unchanged. `Flight` and `Seat` have no seat-class field, so
  `seat_class` is omitted rather than guessed or added.
- Update shared-base templates, routes/views as needed, tests, README documentation, repository
  guidance where its Exercise 5 scope is stale, and OpenSpec requirements.
- Cover GitHub issues #11, #12, and #13.
- Keep authentication UI, payments, interactive seat maps, external airline APIs, a complete
  multi-step booking workflow, and production styling out of scope.

## Capabilities

### New Capabilities

- `reservation-forms`: Defines validated GET flight search and POST guest-booking form behavior,
  including error retention, persistence, duplicate-seat handling, CSRF, and redirects.

### Modified Capabilities

- `basic-reservation-views`: Replaces the unfiltered flight list and non-persisting placeholder
  booking contract with form-backed search and booking endpoints.
- `django-project-foundation`: Updates the exercise boundary to permit the narrowly scoped
  Exercise 8 search and booking forms while retaining the remaining deferred features.
- `repository-agent-guidance`: Updates contributor guidance from the Exercise 5 boundary to the
  Exercise 8 forms scope and verification expectations.

## Impact

The change affects `reservations/forms.py`, reservation views and URLs, templates extending the
shared `base.html`, view/form tests, `README.md`, `AGENTS.md` if its scope statement remains stale,
and the listed OpenSpec capabilities. It adds no framework or service dependency and should
produce no model or migration changes. The existing unique constraint on `Booking.seat` remains
the final server-side safeguard against stale or concurrent duplicate booking attempts.
