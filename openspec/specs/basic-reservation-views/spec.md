# Basic Reservation Views Specification

## Purpose

Define SkyBook's basic public HTTP views, URL contracts, validated search and booking
behavior, and contributor-facing endpoint documentation.

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
The `flight_list` view SHALL accept GET requests at `/flights/`, render a Django
flight-search form in `reservations/flight_list.html`, and expose the result as the
`flights` template context value. Without query parameters it SHALL query all
`Flight` objects ordered by ascending `departure_time`. With valid query parameters
it SHALL expose only flights matching the validated origin, destination, and
departure date in that order. With invalid submitted query parameters it SHALL
render visible form errors and no partially filtered result set.

#### Scenario: Visitor lists flights without searching
- **WHEN** a visitor sends GET `/flights/` without query parameters and flights have
  different departure times
- **THEN** the response has status 200, uses `reservations/flight_list.html`, and its
  `flights` context contains all flights in ascending departure-time order

#### Scenario: Visitor searches flights
- **WHEN** a visitor sends GET `/flights/` with a valid origin, destination, and
  departure date
- **THEN** the response has status 200 and its `flights` context contains only
  matching flights in ascending departure-time order

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

### Requirement: Booking form
The `booking_new` view SHALL accept GET requests at `/booking/new/` and render
`reservations/booking_form.html` with an unbound Django booking form containing
required `seat`, `passenger_name`, and `passenger_email` fields. The HTML form SHALL
submit by POST to the named booking-submission route and SHALL include CSRF
protection.

#### Scenario: Visitor opens the booking form
- **WHEN** a visitor sends GET `/booking/new/`
- **THEN** the response has status 200, uses `reservations/booking_form.html`, and
  contains the three required booking field names and a CSRF token

### Requirement: Booking submission
The `booking_submit` view SHALL accept POST requests at `/booking/submit/`, bind
`request.POST` to the Django booking form, and create a guest `Booking` only for
valid data. Invalid data SHALL create no booking and SHALL redisplay
`reservations/booking_form.html` with visible errors and retained submitted values.
A successful submission SHALL redirect to the named home route.

#### Scenario: Booking fields are valid
- **WHEN** a visitor POSTs an available existing seat, non-empty passenger name, and
  valid passenger email
- **THEN** the response redirects to the named home route with status 302 and
  exactly one guest booking is persisted

#### Scenario: A booking field is invalid
- **WHEN** a visitor POSTs a missing, malformed, unknown, or unavailable booking
  value
- **THEN** the response has status 200, uses `reservations/booking_form.html`,
  reports visible form errors, retains submitted values, and persists no booking

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
Contributor documentation SHALL describe each public endpoint's URL, method, path
arguments, form fields, validation rules, return behavior, status codes, persistence
behavior, and redirects. It SHALL document that an empty flight search shows all
flights, that seat class is omitted because the model does not support it, and that
successful booking submission creates a guest booking.

#### Scenario: Contributor reviews the HTTP contract
- **WHEN** a contributor reads `README.md`
- **THEN** the public endpoints and the Exercise 8 search and booking form contracts
  are documented

### Requirement: Semantic public view presentation
The existing home, flight-list, flight-detail, and booking-form views SHALL render
their content with page-appropriate semantic HTML while preserving their named routes,
request methods, context values, form actions, response statuses, search results, and
booking outcomes.

#### Scenario: Visitor opens the home page
- **WHEN** a visitor sends GET `/`
- **THEN** the response presents the welcome content and destination links in semantic
  page regions without changing either link target

#### Scenario: Visitor views flight results
- **WHEN** a visitor sends GET `/flights/`
- **THEN** the search form and flight-result or empty-state content use appropriate
  semantic elements without changing search behavior

#### Scenario: Visitor views a flight
- **WHEN** a visitor opens an existing flight detail URL
- **THEN** the response presents the existing airline, route, departure, and arrival
  values in an appropriately labeled content region

#### Scenario: Visitor books a flight
- **WHEN** a visitor opens or submits the booking form
- **THEN** the form retains its POST action, CSRF protection, fields, validation, and
  persistence behavior within the improved semantic presentation
