## MODIFIED Requirements

### Requirement: Ordered flight list
The `flight_list` view SHALL accept GET requests at `/flights/`, render a Django
flight-search form in `reservations/flight_list.html`, and expose the result as the
`flights` template context value. Without query parameters it SHALL query all
`Flight` objects ordered by ascending `departure_time`. With valid query parameters
it SHALL expose only flights matching the validated origin, destination, and
departure date in that order. With invalid submitted query parameters it SHALL
render visible form errors and no partially filtered result set. When the request has
an `HX-Request` header value of `true`, the view SHALL return only
`reservations/partials/flight_results.html`; otherwise it SHALL return the complete
flight-list page.

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

#### Scenario: HTMX visitor searches flights
- **WHEN** a visitor sends GET `/flights/` with `HX-Request: true`
- **THEN** the response has status 200, uses
  `reservations/partials/flight_results.html`, and omits the complete page shell
