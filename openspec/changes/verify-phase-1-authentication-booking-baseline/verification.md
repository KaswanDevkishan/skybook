# Phase 1 Baseline Verification

## Scope and result

This record verifies the existing Phase 1 authentication and booking-rule behavior before
Phase 2 restructures the booking journey. The review found equivalent automated coverage
for every normative Phase 1 behavior and security boundary. No coverage gap or runtime
defect was demonstrated, so no application code, template, style, route, setting, model,
migration, seed, dependency, or test change is required by this closure.

## Requirement traceability

| Phase 1 requirement | Responsible implementation | Automated evidence | Result |
| --- | --- | --- | --- |
| Root navigation | `reservations/urls.py` root `RedirectView`; brand link in `reservations/templates/reservations/base.html`; removed `home.html` | `tests/test_views.py::test_root_redirects_to_flights`; `test_flight_search_has_logged_out_navigation_without_old_landing_copy`; authentication navigation tests | Verified |
| Hero simplification | `reservations/templates/reservations/flight_list.html`; obsolete hero rules removed from `reservations/static/reservations/styles.css` | `tests/test_views.py::test_empty_flight_list_has_complete_page_and_search_form`; `test_flight_search_has_logged_out_navigation_without_old_landing_copy`; readable-layout style test | Verified |
| Local departure-date boundary | `reservations/forms.py::FlightSearchForm.__init__` and `clean_departure_date`; `reservations/views.py::flight_list`; full-page template and HTMX results partial | `tests/test_forms.py::test_flight_search_date_input_minimum_is_today`; `test_flight_search_accepts_today_and_future_dates`; `test_flight_search_rejects_yesterday`; `test_flight_search_uses_configured_timezone_local_date`; full-page and HTMX past-date tests in `tests/test_views.py` | Verified |
| Single accessible login error | `reservations/forms.py::SignInForm`; `reservations/templates/reservations/sign_in.html`; auth error styles in `styles.css` | `tests/test_authentication.py::test_failed_sign_in_shows_one_friendly_accessible_alert`; `test_required_sign_in_field_errors_stay_associated_with_inputs`; auth responsive-style test | Verified |
| Authentication gate | `reservations/views.py::flight_booking`, `resume_booking`, and authenticated confirmation branch; anonymous actions in `booking_form.html` | `tests/test_authentication.py::test_logged_out_booking_preserves_pending_details_without_creating_booking`; `test_seat_selection_actions_follow_authentication_state`; `test_direct_logged_out_review_and_confirmation_are_blocked`; booking review/confirmation tests in `tests/test_views.py` | Verified |
| Pending booking resume | `reservations/pending_booking.py`; `SignInView.get_success_url`; registration and resume views; server price calculation | Sign-in and registration resume tests; current-database-price test; successful cleanup test; missing/unavailable and malformed-session cleanup tests in `tests/test_authentication.py` | Verified |
| Passenger-email independence | Editable `BookingForm`; authenticated initial values in `flight_booking`; no user lookup in booking form, pending-booking module, views, or service | `tests/test_authentication.py::test_authenticated_booking_prefills_and_preserves_edits`; `test_unregistered_passenger_email_can_be_booked_by_authenticated_user`; `test_passenger_email_never_discloses_account_existence` | Verified |
| Required public ownership | `flight_booking` passes `request.user`; `reservations/services.py::create_booking` assigns the owner inside the transaction; `Booking` preserves nullable historical ownership | `tests/test_views.py::test_confirm_creates_owned_booking_and_redirects_to_detailed_receipt`; `tests/test_authentication.py::test_service_assigns_optional_owner`; direct-anonymous blocking and receipt-authorization tests | Verified |
| Active-only My Bookings | Confirmed-and-owner filter in `reservations/views.py::account`; empty state and Find a flight action in `account.html` | `tests/test_authentication.py::test_account_history_only_displays_owned_bookings`; account access/navigation tests; cancellation redirect/empty-state assertions | Verified |
| Status-based cancellation | `reservations/views.py::cancel_booking`; conditional Confirmed-seat constraint in `reservations/models.py`; Confirmed-only availability in forms, queries, seat map, and booking service; cancellation template | All eight tests in `tests/test_cancellation.py`, covering GET safety, CSRF POST, owner scope, retained snapshots, released inventory, future-only rejection, repeated cancellation, and owner-only cancelled receipts | Verified |
| Historical guest preservation | Nullable `Booking.user`; guest-or-owner visibility rule in `booking_confirmation`; migration preservation tests | `tests/test_authentication.py::test_booking_receipts_enforce_owner_and_preserve_guest_access`; migration tests in `tests/test_migrations.py`; historical model constraint tests | Verified |
| End-to-end verification | Repository commands and strict OpenSpec contracts | Complete Pytest suite, Ruff, Django checks, migration drift, strict OpenSpec validation, and diff checks recorded below | Pending quality-gate run |

## Security and preservation boundary review

| Boundary | Evidence | Finding |
| --- | --- | --- |
| Anonymous creation is impossible | Anonymous valid submissions store pending data and redirect to authentication; direct review/confirmation tests assert zero bookings | Covered |
| Pending session data is allowlisted | `load_pending_booking` requires exactly version, flight ID, seat ID, passenger name, and passenger email; tests inspect payload and malformed cleanup | Covered |
| Password, payment, and browser price data are excluded | The pending payload is constructed solely from validated form/domain values and rejects extra keys | Covered |
| Pending objects remain flight-scoped and available | Loader checks flight/seat existence and relationship; the bound resume form excludes Confirmed seats; stale-seat tests cover cleanup | Covered |
| Redirects remain local | Django `LoginView` applies allowed-host validation; the test covers valid local, external, and protocol-relative `next`; pending resume uses a fixed named route | Covered |
| Passenger email reveals no account membership | Booking code never queries the user table by passenger email; tests compare registered and unregistered inputs and exclude disclosure copy | Covered |
| New public booking ownership is atomic | The authenticated user is passed into transactional creation and stored with the booking; anonymous direct paths are blocked | Covered |
| Receipt visibility prevents cross-user disclosure | Owned receipts filter by requester; historical guest receipts retain high-entropy-reference access; tests exercise anonymous, owner, and other-user cases | Covered |
| Cancellation is idempotent and non-destructive | Row locking plus status transition retains the row/snapshots; repeated POST returns safely | Covered |
| Cancelled seats return to inventory | Conditional database uniqueness and all availability queries count only Confirmed bookings; search, form, and rebooking assertions exist | Covered |
| Cancellation has no real refund implication | Confirmation template and success message state payment is simulated and no real refund occurs; tests assert the notice | Covered |
| SQLite/PostgreSQL compatibility is retained | Django conditional constraint, environment settings tests, migration tests, and Render configuration remain unchanged | Covered |

## Coverage-gap decision

No normative Phase 1 scenario lacks equivalent automated coverage. Adding tests would
duplicate existing assertions without increasing protection, so tasks 2.1 and 2.2 are
satisfied by reusing the tests listed above and making no test edits. No runtime defect
was found, so the stop-and-revise condition in task 2.3 was not triggered.

## Phase 2 preservation baseline

The Phase 2 OpenSpec change must preserve these invariants:

- Django remains the only server framework; normal form submission remains functional
  alongside existing strict `HX-Request: true` behavior.
- Search accepts today or future dates only and keeps the exact field-level past-date
  message in complete-page and HTMX responses.
- Anonymous visitors may choose a flight and seat and enter editable passenger details,
  but cannot review price, enter payment, or create a Booking before authentication.
- Server-side workflow state stores only allowlisted flight, seat, passenger name, and
  passenger email data; it never stores passwords, payment fields, or submitted prices.
- Authentication resume uses local routes, revalidates flight-scoped availability, and
  recalculates JPY prices from current database values.
- Passenger details remain independent from account identity and never reveal whether an
  email belongs to an account.
- Every new public Booking is assigned to `request.user` within the final transaction.
- Historical null-owner guest bookings and their receipt access remain intact.
- Owner-only registered receipts, active-only My Bookings, CSRF-protected POST logout,
  and CSRF-protected owner-only future cancellation remain enforced.
- Cancelled rows remain stored, do not occupy inventory, and never imply a real refund.
- Cross-flight injection, stale selection, duplicate booking, and browser-supplied price
  authority remain rejected by server validation and database constraints.
- SQLite development, Render PostgreSQL, WhiteNoise, secure production settings, and the
  existing health/deployment paths remain unchanged.

## Quality-gate evidence

Quality-gate results are recorded here after all prescribed commands complete.

- `uv run ruff format --check .`: passed; 135 files already formatted.
- `uv run ruff check .`: passed with no lint errors.
- `uv run pytest`: passed; 154 tests and 94% total coverage, matching the audited
  baseline with no regression.
- `uv run python manage.py check`: passed with no issues.
- `uv run python manage.py makemigrations --check --dry-run`: passed; no changes
  detected.
- `openspec validate verify-phase-1-authentication-booking-baseline --strict`: passed.
- `git diff --check`: passed.

The final scope review found that this application session changed only this change's
verification record and task checkboxes. It added no test because no coverage gap was
demonstrated. The application, templates, styles, routes, settings, models, existing
tests, dependencies, seed data, and production configuration were not modified.

The repository already contained an uncommitted `reservations/migrations/0004_booking_status.py`
and other authentication/ownership working-tree changes before this apply session; they
remain user-owned and untouched. Migration drift reports no changes. `HEAD` remains
`ec4dd53fa888136cf8d3bae38f1a61df199eaa71`. No commit, push, archive, merge, or
deployment command was run.
