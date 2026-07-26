## Context

The current `/flights/` view always lists every flight, and booking uses separate GET and POST
views with handwritten string checks that never persist a record. The existing data model already
contains every field needed for Exercise 8: `Flight.origin`, `Flight.destination`,
`Flight.departure_time`, `Booking.seat`, `Booking.guest_name`, and `Booking.guest_email`.
`Booking.seat` is protected by the `unique_booking_per_seat` database constraint.

This change spans Django forms, query construction, persistence, views, URLs, templates, tests,
and contributor specifications. The existing templates already extend the shared
`reservations/base.html`.

## Goals / Non-Goals

**Goals:**

- Validate flight-search and guest-booking input with Django forms.
- Use GET for bookmarkable search queries and POST plus CSRF for state-changing booking requests.
- Preserve submitted values and expose field and non-field errors in the rendered templates.
- Create valid guest bookings while retaining database-backed duplicate-seat protection.
- Keep current model field names, dependencies, and schema unchanged.
- Document Exercise 8 behavior and cover GitHub issues #11, #12, and #13.

**Non-Goals:**

- Authentication UI or a registered-user booking flow.
- Seat classes, because the current `Flight` and `Seat` models do not represent them.
- Payments, external airline APIs, interactive seat maps, a multi-step booking workflow, or
  production styling.

## Decisions

### Use explicit Django `Form` classes

`FlightSearchForm` will use `ModelChoiceField` values for `origin` and `destination` plus a
`DateField` for `departure_date`. A custom `clean()` method will reject identical cities.
`BookingForm` will use a `ModelChoiceField` for `seat`, `CharField` for `passenger_name`, and
`EmailField` for `passenger_email`.

Explicit forms keep the public passenger field names required by Exercise 8 while allowing the
save path to map them deliberately to `Booking.guest_name` and `Booking.guest_email`. A
`ModelForm` was considered, but it would either expose model-centric guest field names or require
additional aliasing with little benefit.

### Treat an empty search as an unfiltered list

The flight-list view will construct the form from `request.GET` when query data is present. An
initial GET with no query parameters will show every flight ordered by `departure_time`. A valid
submitted search will filter by exact origin and destination and by
`departure_time__date`, then retain the same ordering. An invalid submitted search will render
the bound form and its errors without applying partial filters.

Showing all flights on the initial page preserves the current endpoint behavior and gives users
useful content before searching. Showing no partial-filter result for invalid data avoids
presenting a result set as though an invalid search succeeded.

### Keep booking availability validation and database enforcement

`BookingForm` will verify that the selected `Seat` resolves through its model-choice queryset and
does not currently have a booking. Valid POST handling will create a guest `Booking` from
`cleaned_data`. The database unique constraint remains authoritative for stale or concurrent
requests.

The view will save inside an atomic transaction and translate a duplicate-seat `IntegrityError`
from a race into a visible seat error without creating another booking. Relying only on the
form-time availability query was rejected because it cannot close the concurrency window.

### Preserve the existing route surface

`booking_new` will render an unbound form for GET and `booking_submit` will bind POST data, which
retains the existing named URLs and keeps method behavior explicit. Successful booking will
redirect to the named home route. Invalid POST responses will render the shared booking template
with status 200, matching conventional Django form redisplay behavior.

### Render fields and errors explicitly

Templates will continue to extend `reservations/base.html`, render labels and fields, show each
field's errors near that field, show non-field errors, and include CSRF in the booking form.
Django's bound-form widgets will retain submitted values without manual context variables.

## Risks / Trade-offs

- [A seat can be booked after form validation but before insert] → Keep the unique database
  constraint, save atomically, and convert the resulting duplicate error into a form error.
- [A broad `IntegrityError` handler could hide unrelated defects] → Limit handling to the booking
  save boundary and only report the expected seat-conflict case; re-raise unexpected failures
  where they can be distinguished.
- [Date filtering depends on Django's active time zone] → Use `departure_time__date` consistently
  and test dates with timezone-aware flight timestamps.
- [Listing every seat includes already-booked choices] → Prefer an available-seat queryset for
  usability, while still validating and enforcing availability server-side for stale or tampered
  submissions.
- [Keeping split booking URLs is less compact than one GET/POST endpoint] → Preserve compatibility
  with the existing named URL contract and avoid an unnecessary route migration.

## Migration Plan

1. Add forms, update views/templates/routes, and replace placeholder tests with form and
   persistence coverage.
2. Update README, repository guidance where needed, and OpenSpec delta specifications.
3. Run formatting, linting, Django checks, migration-drift detection, and the full test suite.
4. Deploy as an application-only change; no database migration is expected.

Rollback consists of reverting the application and documentation changes. Bookings created while
the feature is active remain valid domain records and require no data migration.

## Open Questions

None. The model inspection resolves field mapping and confirms that seat class is unavailable.
