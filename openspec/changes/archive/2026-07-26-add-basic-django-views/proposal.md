## Why

SkyBook has a working Django foundation and reservation schema but no public HTTP
surface for exercising the application. The next course increment needs a deliberately
small set of read-only flight pages, a placeholder booking submission, and a health
endpoint without expanding into the deferred booking workflow.

## What Changes

- Add function-based home, flight-list, flight-detail, booking-form,
  booking-submission, and health views with named URL patterns.
- Add simple Django templates for the public pages and placeholder booking form.
- Define request methods, path arguments, form fields, response content, status codes,
  404 behavior, and successful-submission redirect behavior.
- Add view and URL tests covering templates, context, ordering, reversing, validation,
  redirects, and unsupported methods.
- Document the public routes and verification workflow in `README.md`.
- Keep the reservation schema unchanged and do not persist bookings from the
  placeholder form.
- Keep flight search, authentication pages, payments, interactive seat selection, and
  the complete booking workflow out of scope.

## Capabilities

### New Capabilities

- `basic-reservation-views`: Defines SkyBook's initial public pages, placeholder booking
  form and submission contract, health endpoint, and named URL routes.

### Modified Capabilities

- `django-project-foundation`: Expands the permitted Exercise 5 HTTP surface from the
  generated foundation to the explicitly bounded basic views while retaining the
  deferred-feature boundary.

## Impact

- Affects `reservations/views.py`, new application URL configuration, project URL
  inclusion, application templates, view and URL tests, and `README.md`.
- Uses the existing `Flight` model for ordered list and detail queries.
- Adds no dependencies, migrations, schema changes, authentication, payment handling,
  seat-selection behavior, or booking persistence.
- Relates to GitHub issues #6, #7, and #8.
