## MODIFIED Requirements

### Requirement: Ordered flight list
The `flight_list` view SHALL accept GET requests at `/flights/`, render a Django flight-search
form in `reservations/flight_list.html`, and expose the result as the `flights` template context
value. Without query parameters it SHALL query all `Flight` objects ordered by ascending
`departure_time`. With valid query parameters it SHALL expose only flights matching the validated
origin, destination, and departure date in that order. With invalid submitted query parameters it
SHALL render visible form errors and no partially filtered result set.

#### Scenario: Visitor lists flights without searching
- **WHEN** a visitor sends GET `/flights/` without query parameters and flights have different departure times
- **THEN** the response has status 200, uses `reservations/flight_list.html`, and its `flights` context contains all flights in ascending departure-time order

#### Scenario: Visitor searches flights
- **WHEN** a visitor sends GET `/flights/` with a valid origin, destination, and departure date
- **THEN** the response has status 200 and its `flights` context contains only matching flights in ascending departure-time order

#### Scenario: No flights exist
- **WHEN** a visitor sends GET `/flights/` while no flights exist
- **THEN** the response has status 200 and the `flights` context is empty

### Requirement: Placeholder booking form
The `booking_new` view SHALL accept GET requests at `/booking/new/` and render
`reservations/booking_form.html` with an unbound Django booking form containing required `seat`,
`passenger_name`, and `passenger_email` fields. The HTML form SHALL submit by POST to the named
booking-submission route and SHALL include CSRF protection.

#### Scenario: Visitor opens the booking form
- **WHEN** a visitor sends GET `/booking/new/`
- **THEN** the response has status 200, uses `reservations/booking_form.html`, and contains the three required booking field names and a CSRF token

### Requirement: Placeholder booking submission
The `booking_submit` view SHALL accept POST requests at `/booking/submit/`, bind
`request.POST` to the Django booking form, and create a guest `Booking` only for valid data.
Invalid data SHALL create no booking and SHALL redisplay `reservations/booking_form.html` with
visible errors and retained submitted values. A successful submission SHALL redirect to the named
home route.

#### Scenario: Booking fields are valid
- **WHEN** a visitor POSTs an available existing seat, non-empty passenger name, and valid passenger email
- **THEN** the response redirects to the named home route with status 302 and exactly one guest booking is persisted

#### Scenario: A booking field is invalid
- **WHEN** a visitor POSTs a missing, malformed, unknown, or unavailable booking value
- **THEN** the response has status 200, uses `reservations/booking_form.html`, reports visible form errors, retains submitted values, and persists no booking

#### Scenario: Submission endpoint receives an unsupported method
- **WHEN** a caller requests `/booking/submit/` with a method other than POST
- **THEN** the response has status 405

### Requirement: Public route documentation
Contributor documentation SHALL describe each public endpoint's URL, method, path arguments,
form fields, validation rules, return behavior, status codes, persistence behavior, and redirects.
It SHALL document that an empty flight search shows all flights, that seat class is omitted
because the model does not support it, and that successful booking submission creates a guest
booking.

#### Scenario: Contributor reviews the HTTP contract
- **WHEN** a contributor reads `README.md`
- **THEN** the public endpoints and the Exercise 8 search and booking form contracts are documented
