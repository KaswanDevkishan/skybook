# Reservation Forms Specification

## Purpose

Define SkyBook's validated GET flight-search and POST guest-booking forms, including
result filtering, error handling, persistence, CSRF protection, and duplicate-seat
safety.

## Requirements

### Requirement: Validated flight search form
The system SHALL provide a Django `FlightSearchForm` with required `origin`,
`destination`, and `departure_date` fields. Origin and destination SHALL resolve to
existing `City` records and MUST be different. The form SHALL omit `seat_class`
while the current data model has no compatible seat-class field.

#### Scenario: Visitor opens flight search
- **WHEN** a visitor sends GET `/flights/` without query parameters
- **THEN** the response renders an unbound search form with origin, destination, and
  departure-date fields

#### Scenario: Visitor submits the same city
- **WHEN** a visitor submits the same existing city as origin and destination
- **THEN** the bound search form is invalid and displays a route validation error

#### Scenario: Visitor submits an invalid date
- **WHEN** a visitor submits a departure date that Django cannot parse as a date
- **THEN** the bound search form is invalid and displays a departure-date error

#### Scenario: Visitor submits missing search input
- **WHEN** a visitor submits a search with a required field missing
- **THEN** the bound search form is invalid and displays the required-field error

### Requirement: Validated search controls flight results
The flight-list view SHALL bind submitted GET query data to `FlightSearchForm` and
SHALL only filter from `cleaned_data` after successful validation. A valid search
SHALL match exact origin and destination records and the calendar date of
`departure_time`, order matches by ascending `departure_time`, and preserve submitted
query values. A request without query parameters SHALL show all flights in that
order; an invalid submitted search SHALL show no filtered results.

#### Scenario: Valid query filters flights
- **WHEN** a visitor submits valid origin, destination, and departure-date values
- **THEN** the response contains only matching flights ordered by ascending
  departure time

#### Scenario: Initial search is unfiltered
- **WHEN** a visitor opens `/flights/` without query parameters
- **THEN** all flights are available in ascending departure-time order

#### Scenario: Invalid search does not apply partial filters
- **WHEN** a visitor submits an invalid search
- **THEN** the response displays the bound form errors and does not present partially
  filtered flights

#### Scenario: Search input is retained
- **WHEN** a visitor submits valid or invalid search query values
- **THEN** the rendered bound form retains those submitted values

### Requirement: Validated guest booking form
The system SHALL provide a Django `BookingForm` with required `seat`,
`passenger_name`, and `passenger_email` fields. The email field MUST use Django email
validation, the seat MUST resolve to an existing `Seat`, and the selected seat MUST
have no existing booking.

#### Scenario: Visitor opens booking form
- **WHEN** a visitor sends GET `/booking/new/`
- **THEN** the response renders an unbound form with seat, passenger-name, and
  passenger-email fields

#### Scenario: Visitor submits a valid email
- **WHEN** a visitor submits a syntactically valid email with other valid booking data
- **THEN** email validation succeeds

#### Scenario: Visitor submits an invalid email
- **WHEN** a visitor submits a malformed passenger email
- **THEN** the form is invalid and displays an email error

#### Scenario: Visitor submits a missing or unknown seat
- **WHEN** a visitor omits the seat or submits a seat identifier that does not exist
- **THEN** the form is invalid and displays a seat error

#### Scenario: Visitor submits an already-booked seat
- **WHEN** a visitor submits a seat that already has a `Booking`
- **THEN** the form is invalid and displays a seat-availability error

### Requirement: Valid booking submission persists safely
The booking submission endpoint SHALL accept POST data, bind it to `BookingForm`, and
create a guest `Booking` only when the form is valid. It SHALL map `passenger_name` to
`guest_name`, `passenger_email` to `guest_email`, leave `user` null, and redirect to
the named home route after success. It MUST retain the existing database constraint
preventing more than one booking for a seat and SHALL report a duplicate-seat
conflict caused by stale or concurrent input as a visible form error.

#### Scenario: Valid guest booking succeeds
- **WHEN** a visitor POSTs an available seat, passenger name, and valid passenger
  email
- **THEN** exactly one guest booking is created with the submitted values and the
  response redirects to home

#### Scenario: Invalid booking creates nothing
- **WHEN** a visitor POSTs invalid booking data
- **THEN** no booking is created and the bound form is redisplayed with errors and
  retained values

#### Scenario: Concurrent duplicate is rejected
- **WHEN** two stale or concurrent valid submissions attempt to book the same seat
- **THEN** the database permits at most one booking and the losing submission
  receives a visible seat error

### Requirement: Booking submissions are CSRF protected
The booking template SHALL submit with POST and include Django's CSRF token, and the
booking submission endpoint MUST reject a POST request without a valid CSRF token
when CSRF checks are enforced.

#### Scenario: Booking form includes CSRF token
- **WHEN** a visitor opens the booking form
- **THEN** the rendered POST form contains a CSRF token

#### Scenario: Missing CSRF token is rejected
- **WHEN** a client with CSRF enforcement POSTs booking data without a valid token
- **THEN** Django returns status 403 and creates no booking
