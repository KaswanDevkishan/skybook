## ADDED Requirements

### Requirement: Flight searches accept only current or future local dates
The flight-search departure-date input SHALL expose a `min` attribute equal to
`timezone.localdate()` at form construction time. The form MUST independently reject a
submitted departure date earlier than `timezone.localdate()` with the field-level
message “Departure date cannot be in the past.” The boundary SHALL respect `USE_TZ` and
the configured project timezone without hardcoded dates. Today and future dates SHALL
remain valid.

The date input SHALL reference the validation message through `aria-describedby`.
Complete-page and strict `HX-Request: true` responses SHALL expose the same accessible
field error without a popup alert.

#### Scenario: Browser receives the current local minimum
- **WHEN** the flight-search form is rendered
- **THEN** the departure-date input has `min` equal to Django's current local date

#### Scenario: Visitor submits a past date
- **WHEN** the submitted departure date is earlier than Django's current local date
- **THEN** form validation rejects it with the associated field message “Departure date
  cannot be in the past.”

#### Scenario: Visitor submits today or a future date
- **WHEN** the submitted departure date is equal to or later than Django's current local
  date
- **THEN** the departure-date field accepts it

#### Scenario: Local date differs from the UTC date
- **WHEN** the configured project timezone places the current instant on a different
  calendar date from UTC
- **THEN** the input minimum and validation boundary use the configured local date

### Requirement: Authentication forms preserve Django validation
The application SHALL render Django-backed registration and sign-in forms with visible
labels, stable control IDs, safe retained non-password values, field-level errors, and an
announced validation summary. Registration MUST use the configured Django password
validators and email validation.

#### Scenario: Authentication input is invalid
- **WHEN** a visitor submits an invalid registration or sign-in form
- **THEN** the bound form displays accessible errors, preserves safe fields, and does not
  render submitted password values

#### Scenario: Sign-in errors remain separated
- **WHEN** a sign-in submission has field-specific and non-field authentication errors
- **THEN** each field-specific error renders directly beneath and remains associated with
  its input while the non-field authentication error renders only once in the top alert

### Requirement: Booking form supports initial account passenger values
The flight-scoped booking form SHALL accept initial passenger name and email values for an
authenticated user's unbound form without changing field validation, seat scoping, or the
meaning of bound POST data.

#### Scenario: Authenticated booking form is initially constructed
- **WHEN** the booking view supplies account passenger defaults on GET
- **THEN** those values render as editable initials and available seat validation is
  unchanged

#### Scenario: Bound passenger values differ from initials
- **WHEN** a user submits edited passenger values
- **THEN** form validation uses and retains the submitted values rather than the initials

### Requirement: Passenger email validation does not inspect accounts
The flight-scoped booking form SHALL validate passenger email syntax without querying
User records, requiring an account match, or producing account-existence feedback.

#### Scenario: Valid passenger email is not registered
- **WHEN** an authenticated user submits a syntactically valid email absent from User
  records
- **THEN** the booking form accepts it without displaying “Email not registered”

#### Scenario: Valid passenger email belongs to another account
- **WHEN** an authenticated user submits a syntactically valid email used by another User
- **THEN** form behavior does not disclose that account and preserves the passenger value
