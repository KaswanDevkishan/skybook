## MODIFIED Requirements

### Requirement: Named reservation URL surface
The application SHALL expose public views through the `reservations` URL namespace
with named patterns for `home`, `flight_list`, `flight_detail`, a flight-specific
booking workflow, booking confirmation by reference, and `health`. The project SHALL
include those routes at its root and SHALL NOT expose the former generic
`booking_new` or `booking_submit` routes.

#### Scenario: Caller reverses a static application route
- **WHEN** a caller reverses `home`, `flight_list`, or `health`
- **THEN** Django returns `/`, `/flights/`, or `/health/` respectively

#### Scenario: Caller reverses a flight route
- **WHEN** a caller reverses flight detail or booking with a flight integer
- **THEN** Django returns the corresponding `/flights/<flight_id>/` or
  `/flights/<flight_id>/book/` path

#### Scenario: Caller reverses confirmation
- **WHEN** a caller reverses booking confirmation with a valid reference
- **THEN** Django returns the reference-specific confirmation path

### Requirement: Home page navigation
The `home` view SHALL accept GET requests at `/`, render `reservations/home.html`, and
present the SkyBook brand as a link to the homepage. The shared primary navigation
SHALL omit a separate Home item and SHALL contain Flights as its only navigation item.
It MUST NOT contain Booking Form, Sign in, account, or other placeholder navigation.
Authentication navigation is deferred to a separate future change.

#### Scenario: Visitor opens the home page
- **WHEN** a visitor sends GET `/`
- **THEN** the response has status 200, the SkyBook brand links to `/`, Flights is the
  only primary navigation item, and no separate Home item appears

#### Scenario: Authentication is not implemented
- **WHEN** a visitor inspects the shared primary navigation
- **THEN** it contains no functional, disabled, or placeholder Sign in or account item

### Requirement: Ordered flight list
The `flight_list` view SHALL accept GET requests at `/flights/`, render the validated
flight-search form, and expose flights ordered by departure time. It SHALL enrich each
result with airline, flight number, route, times, duration, nonstop state, available
seat count, lowest available price, and practical cabin availability. Valid search,
invalid search, empty results, and strict `HX-Request: true` partial behavior SHALL
remain unchanged.

#### Scenario: Visitor lists flights
- **WHEN** matching flights have different departure times and seat availability
- **THEN** results are ordered by departure and contain authoritative schedule and
  availability presentation

#### Scenario: HTMX visitor searches flights
- **WHEN** a visitor sends GET `/flights/` with `HX-Request: true`
- **THEN** the response uses the reusable results partial with the same enriched result
  content and omits the page shell

#### Scenario: Invalid search is submitted
- **WHEN** submitted search data is invalid
- **THEN** visible form errors are returned and no partially filtered flights appear

## REMOVED Requirements

### Requirement: Booking form
**Reason**: The generic `/booking/new/` page exposes seats across flights and is
replaced by the selected flight's booking workflow.

**Migration**: Follow a flight result's Book action or visit
`/flights/<flight_id>/book/` for a valid flight.

### Requirement: Booking submission
**Reason**: The generic `/booking/submit/` endpoint is replaced by reviewed,
flight-scoped confirmation with authoritative pricing.

**Migration**: Submit passenger and seat data through the selected flight's booking
route and follow its confirmation redirect.

## ADDED Requirements

### Requirement: Flight booking and confirmation views
The flight booking view SHALL render seat selection on GET, validate and render price
review on a valid review POST, and atomically create then redirect on a valid final
confirmation POST. The confirmation view SHALL resolve a booking by reference and
render its receipt; missing flights or references SHALL return 404.

#### Scenario: Visitor progresses through valid workflow
- **WHEN** the visitor selects a seat, provides valid guest details, reviews, and
  confirms while the seat remains available
- **THEN** the views create exactly one booking and finish on its confirmation receipt

#### Scenario: Unsupported workflow request occurs
- **WHEN** a caller uses a method not supported by the booking or confirmation view
- **THEN** the view returns the appropriate method-not-allowed response and creates no
  booking

### Requirement: Public route documentation
Contributor documentation SHALL describe current public URLs, methods, arguments,
form actions, validation, status codes, persistence, redirects, flight-scoped entry,
the JPY fee rule, and confirmation behavior. It SHALL document guest booking and the
absence of real payment processing.

#### Scenario: Contributor reviews the HTTP contract
- **WHEN** a contributor reads `README.md`
- **THEN** the connected booking journey and its security and pricing boundaries are
  documented without advertising removed generic endpoints
