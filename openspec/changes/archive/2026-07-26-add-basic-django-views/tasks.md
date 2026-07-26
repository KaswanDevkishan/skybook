## 1. HTTP Contract Tests

- [x] 1.1 Add URL reversing tests for every namespaced static route and the
  `flight_detail` route with its `flight_id` argument.
- [x] 1.2 Add home and health endpoint tests covering status codes, template and link
  rendering, plain-text content type, and response body.
- [x] 1.3 Add database-aware flight list and detail tests covering template names,
  context keys, departure ordering, required rendered fields, empty results, and a
  missing-flight 404.
- [x] 1.4 Add booking form and submission tests covering form fields, CSRF-aware
  rendering, successful redirect without persistence, missing/empty/whitespace
  validation with status 400 and retained input, and unsupported methods with status
  405.

## 2. Views and Routing

- [x] 2.1 Implement the six function-based views in `reservations/views.py` with the
  specified queries, context names, validation, status codes, content type, and
  redirect behavior.
- [x] 2.2 Create namespaced, named patterns in `reservations/urls.py` for the exact
  public paths and include them at the root from `skybook/urls.py`.
- [x] 2.3 Confirm that the implementation introduces no model, migration, booking
  persistence, search/filtering, authentication, payment, or seat-selection behavior.

## 3. Templates

- [x] 3.1 Create `reservations/home.html` with links reversed to the flight list and
  booking form.
- [x] 3.2 Create `reservations/flight_list.html` and
  `reservations/flight_detail.html` to render the specified flight context and detail
  fields.
- [x] 3.3 Create `reservations/booking_form.html` with CSRF protection, the two named
  passenger fields, retained submitted values, validation errors, and a form action
  reversed to the submission route.

## 4. Documentation

- [x] 4.1 Update `README.md` with each endpoint's URL, method, path arguments, form
  fields, return behavior, status codes, redirect target, and non-persistent
  placeholder scope.
- [x] 4.2 Ensure README scope notes continue to exclude flight search, authentication
  pages, payments, interactive seat selection, and the complete booking workflow.

## 5. Verification

- [x] 5.1 Run `uv run ruff format .` and `uv run ruff format --check .`.
- [x] 5.2 Run `uv run ruff check .`.
- [x] 5.3 Run `uv run python manage.py check` and
  `uv run python manage.py makemigrations --check`.
- [x] 5.4 Run `uv run pytest` and confirm configured coverage does not regress.
- [x] 5.5 Run
  `openspec validate add-basic-django-views --type change --strict --no-interactive`
  and review the final diff for scope compliance.
