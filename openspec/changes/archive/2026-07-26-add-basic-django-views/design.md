## Context

SkyBook currently has generated Django project wiring and persisted reservation models,
but its public URL configuration exposes no application pages. This change crosses the
project URL configuration, the `reservations` application, templates, tests, and
contributor documentation. It must use the existing `Flight` schema and remain a small
course-project increment rather than beginning the real booking workflow.

## Goals / Non-Goals

**Goals:**

- Establish a namespaced, named URL surface for six function-based Django views.
- Render basic server-side templates for navigation, flight display, and placeholder
  passenger input.
- Specify predictable query, validation, 404, 405, 400, and redirect behavior.
- Cover the public contract through focused Django/Pytest tests and document it for
  contributors.

**Non-Goals:**

- Flight searching or filtering, authentication pages, payment handling, interactive
  seat selection, or a complete booking workflow.
- Creating `Booking` records or selecting a flight or seat during placeholder
  submission.
- Introducing a Django `Form` class, client-side validation framework, API layer, new
  dependency, or database migration.

## Decisions

### Use an application URL namespace included at the project root

`reservations/urls.py` will declare `app_name = "reservations"` and names for `home`,
`flight_list`, `flight_detail`, `booking_new`, `booking_submit`, and `health`.
`skybook/urls.py` will include those patterns at the empty prefix so the specified
public paths remain exact while callers reverse stable names such as
`reservations:flight_detail`.

An unnamespaced application include was considered, but namespacing prevents collisions
as the course project grows without changing the requested paths.

### Keep views explicit and function-based

Each endpoint will be a small function in `reservations/views.py`. Read-only views will
render directly, flight detail will use `get_object_or_404`, and the submission view
will explicitly reject non-POST requests with HTTP 405.

Class-based generic views were considered, but function-based views are required and
make the small method and validation contract visible.

### Treat booking input as non-persistent placeholder data

The booking template will post `passenger_name` and `passenger_email` to the named
submission URL and include CSRF protection. Submission will strip surrounding
whitespace from both fields. If either resulting value is empty, it will render the
same booking template with HTTP 400, field-specific error context, and the submitted
values. Otherwise it will redirect to the named home URL without creating a model
instance.

A Django `Form` and `Booking` creation were considered, but both would imply validation
and workflow decisions—flight, seat, identity, duplicate handling—not authorized by
this increment.

### Expose simple, stable template context

The flight list will query `Flight.objects.order_by("departure_time")` and expose the
queryset as `flights`. Flight detail will expose one object as `flight`; its template
will display airline, origin and destination, departure time, and arrival time. Home
will link to the named flight-list and booking-form routes.

Adding eager-loading or a service layer was considered, but the small read-only pages
do not yet justify additional abstraction.

### Test the HTTP contract at the Django boundary

Tests will use Django's test client and URL reversing to verify exact route resolution,
methods, status codes, templates, context, ordering, rendered detail fields, missing
flight 404s, invalid and valid POST behavior, redirects, and plain-text health output.
No migration tests are needed because the schema must remain unchanged; the migration
drift check will enforce that decision.

## Risks / Trade-offs

- [The placeholder accepts any non-empty email string] → Document that this increment
  validates presence only and defer email-shape validation to a future form workflow.
- [A list page could be mistaken for flight search] → Provide no query parameters,
  filtering, search controls, or availability logic.
- [The successful POST discards passenger data] → Make the behavior explicit in the
  template, README, spec, and tests; do not imply that a booking was created.
- [Template details can make tests brittle] → Assert required content and template
  names rather than full HTML snapshots.
- [Future booking implementation will replace this contract] → Keep URL names stable
  where practical, while treating persistence and richer validation as a separately
  proposed change.

