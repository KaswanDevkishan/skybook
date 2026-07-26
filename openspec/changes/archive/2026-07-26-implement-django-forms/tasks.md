## 1. Django Forms

- [x] 1.1 Create `reservations/forms.py` with `FlightSearchForm` using existing `City` fields, a date input, required-field validation, and distinct-origin/destination validation.
- [x] 1.2 Add `BookingForm` with existing-seat selection, required passenger name, Django email validation, and already-booked-seat validation.
- [x] 1.3 Map the booking form's public passenger fields to `Booking.guest_name` and `Booking.guest_email` without changing the model schema.

## 2. Search and Booking Views

- [x] 2.1 Bind flight search from GET query data, show all ordered flights for an empty search, and filter valid searches by origin, destination, and departure date using `cleaned_data`.
- [x] 2.2 Render an unbound booking form on GET and bind `request.POST` on the existing POST submission endpoint.
- [x] 2.3 Create a valid guest `Booking` atomically, redirect to the named home route, and preserve the database constraint as the final duplicate-seat safeguard.
- [x] 2.4 Redisplay invalid or stale/concurrent duplicate booking submissions with visible form errors and retained input, without creating another booking.

## 3. URLs and Templates

- [x] 3.1 Update reservation URLs only where needed while preserving named route compatibility and GET/POST method boundaries.
- [x] 3.2 Update the flight-list template to extend the shared base, submit search fields with GET, and render bound values plus field and non-field errors clearly.
- [x] 3.3 Update the booking template to extend the shared base, render all booking fields and errors clearly, submit with POST, and include CSRF protection.

## 4. Automated Tests

- [x] 4.1 Add tests for search-form rendering, empty-search ordering, valid GET filtering, retained query values, same-city validation, invalid dates, and required input.
- [x] 4.2 Add tests for unbound booking-form rendering, valid and invalid email behavior, missing or unknown seats, retained values, and visible errors.
- [x] 4.3 Add tests that valid POST data creates the correctly mapped guest booking and redirects after success, while every invalid form creates no booking.
- [x] 4.4 Add tests for pre-existing and stale/concurrent duplicate-seat rejection using the existing database uniqueness constraint.
- [x] 4.5 Add an enforced-CSRF test proving a tokenless booking POST returns 403 and persists no booking.

## 5. Documentation and Specifications

- [x] 5.1 Update `README.md` with issues #11, #12, and #13; form fields and methods; validation; empty-search behavior; persistence; errors; status codes; and redirect targets.
- [x] 5.2 Update `AGENTS.md` to describe the Exercise 8 form scope and remaining non-goals if its Exercise 5 boundary is still stale.
- [x] 5.3 Reconcile the implemented behavior with all change specs and prepare the delta specs for later synchronization.

## 6. Verification

- [x] 6.1 Run `uv run ruff format .` and `uv run ruff check .`.
- [x] 6.2 Run `uv run pytest` and confirm coverage does not decrease.
- [x] 6.3 Run `uv run python manage.py check` and `uv run python manage.py makemigrations --check --dry-run`, confirming no schema drift.
- [x] 6.4 Run `openspec validate implement-django-forms` and resolve all artifact or requirement errors.
