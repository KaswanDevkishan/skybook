# Basic Reservation Views Specification

## Purpose

Define SkyBook's basic public HTTP views, URL contracts, placeholder booking
submission behavior, and contributor-facing endpoint documentation.

## Requirements

### Requirement: Named reservation URL surface
The application SHALL expose its basic views through a `reservations` URL namespace
with named patterns for `home`, `flight_list`, `flight_detail`, `booking_new`,
`booking_submit`, and `health`, and the project SHALL include those routes at its root.

#### Scenario: Caller reverses a static application route
- **WHEN** a caller reverses a static route by its namespaced name
- **THEN** Django returns the corresponding `/`, `/flights/`, `/booking/new/`,
  `/booking/submit/`, or `/health/` path

#### Scenario: Caller reverses flight detail
- **WHEN** a caller reverses `reservations:flight_detail` with a `flight_id` integer
- **THEN** Django returns `/flights/<flight_id>/`

### Requirement: Home page navigation
The `home` view SHALL accept GET requests at `/`, render
`reservations/home.html`, and present links to the named flight-list and booking-form
routes.

#### Scenario: Visitor opens the home page
- **WHEN** a visitor sends GET `/`
- **THEN** the response has status 200, uses `reservations/home.html`, and contains
  links to `/flights/` and `/booking/new/`

### Requirement: Ordered flight list
The `flight_list` view SHALL accept GET requests at `/flights/`, query all `Flight`
objects ordered by ascending `departure_time`, render `reservations/flight_list.html`,
and expose the result as the `flights` template context value.

#### Scenario: Visitor lists flights
- **WHEN** a visitor sends GET `/flights/` and flights have different departure times
- **THEN** the response has status 200, uses `reservations/flight_list.html`, and its
  `flights` context contains those flights in ascending departure-time order

#### Scenario: No flights exist
- **WHEN** a visitor sends GET `/flights/` while no flights exist
- **THEN** the response has status 200 and the `flights` context is empty

### Requirement: Flight detail
The `flight_detail` view SHALL accept GET requests at
`/flights/<int:flight_id>/`, retrieve the identified `Flight`, render
`reservations/flight_detail.html`, and expose it as the `flight` template context
value. The rendered page SHALL show the flight's airline, origin and destination
route, departure time, and arrival time.

#### Scenario: Visitor opens an existing flight
- **WHEN** a visitor sends GET for an existing flight ID
- **THEN** the response has status 200, uses `reservations/flight_detail.html`, and
  renders that flight's airline, route, departure time, and arrival time

#### Scenario: Visitor opens a missing flight
- **WHEN** a visitor sends GET for a flight ID that does not exist
- **THEN** the response has status 404

### Requirement: Placeholder booking form
The `booking_new` view SHALL accept GET requests at `/booking/new/` and render
`reservations/booking_form.html` with a CSRF-protected HTML form containing
`passenger_name` and `passenger_email` fields that submits by POST to the named
booking-submission route.

#### Scenario: Visitor opens the booking form
- **WHEN** a visitor sends GET `/booking/new/`
- **THEN** the response has status 200, uses `reservations/booking_form.html`, and
  contains the two required passenger input field names

### Requirement: Placeholder booking submission
The `booking_submit` view SHALL accept POST requests at `/booking/submit/`, read
`passenger_name` and `passenger_email`, and treat either field as invalid when it is
missing, empty, or contains only whitespace. It SHALL NOT create a `Booking` or other
database record.

#### Scenario: Both passenger fields are valid
- **WHEN** a visitor POSTs non-empty `passenger_name` and `passenger_email`
- **THEN** the response redirects to the named home route with status 302 and no
  booking is persisted

#### Scenario: A passenger field is invalid
- **WHEN** a visitor POSTs with either passenger field missing, empty, or whitespace
- **THEN** the response has status 400, uses `reservations/booking_form.html`, reports
  validation errors in template context, and retains submitted values

#### Scenario: Submission endpoint receives an unsupported method
- **WHEN** a caller requests `/booking/submit/` with a method other than POST
- **THEN** the response has status 405

### Requirement: Plain-text health endpoint
The `health` view SHALL accept GET requests at `/health/` and return a successful
plain-text response suitable for checking that the Django application is running.

#### Scenario: Monitor checks application health
- **WHEN** a monitor sends GET `/health/`
- **THEN** the response has status 200, a plain-text content type, and a non-empty
  health response body

### Requirement: Public route documentation
Contributor documentation SHALL describe each basic endpoint's URL, method, path
arguments, form fields, return behavior, status codes, and redirects, and SHALL state
that placeholder submission does not create a booking.

#### Scenario: Contributor reviews the HTTP contract
- **WHEN** a contributor reads `README.md`
- **THEN** the six endpoints and their request and response contracts are documented
