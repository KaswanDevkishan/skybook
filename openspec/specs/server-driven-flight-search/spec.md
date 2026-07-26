# Server-Driven Flight Search Specification

## Purpose

Define SkyBook's progressively enhanced HTMX flight-search requests, partial response
contract, reusable result rendering, accessible update feedback, and schema boundary.

## Requirements

### Requirement: Pinned declarative HTMX dependency
The shared reservation base template SHALL load a pinned HTMX version for enhanced
requests, SHALL defer that script's execution, and SHALL NOT add a JavaScript framework
or custom JavaScript for the flight search interaction.

#### Scenario: Visitor opens a complete reservation page
- **WHEN** a visitor requests a reservation page that extends the shared base template
- **THEN** the response includes a deferred script URL with an explicit HTMX version

#### Scenario: Contributor reviews the interaction implementation
- **WHEN** a contributor inspects the flight-search implementation
- **THEN** HTMX attributes and server-rendered templates implement the interaction
  without a JavaScript framework or custom request code

### Requirement: Complete GET search requests
The flight-search form SHALL retain `method="get"` and its ordinary action to the named
flight-list route. It SHALL use `hx-get` for the same route, trigger requests when the
origin, destination, or departure-date control changes and when the form is submitted,
and include the complete form values in every enhanced request.

#### Scenario: Visitor changes a search control
- **WHEN** a visitor changes origin, destination, or departure date with HTMX available
- **THEN** the form sends a GET request containing the current values of all three
  controls to the existing flight-list URL

#### Scenario: Visitor submits the enhanced form
- **WHEN** a visitor activates the search submit button with HTMX available
- **THEN** the form sends the complete GET search to the existing flight-list URL

#### Scenario: HTMX is unavailable
- **WHEN** a visitor submits the search form without HTMX
- **THEN** the browser performs an ordinary full-page GET to the existing flight-list
  URL with the submitted values

### Requirement: Targeted result replacement
The enhanced form SHALL target a result region with the stable `flight-results` ID and
SHALL use `innerHTML` swapping so that only the region's contents are replaced. The
node with the stable target ID and its live-region attributes SHALL remain connected
across enhanced updates.

#### Scenario: Enhanced search completes
- **WHEN** the server returns a successful HTMX search response
- **THEN** HTMX replaces only the contents of the flight-results region, leaves its
  live-region owner connected, and leaves the surrounding page and search controls in
  place

### Requirement: Reusable flight-results partial
The system SHALL provide
`reservations/templates/reservations/partials/flight_results.html` as the single
rendering source for the contents of the flight-results region in complete-page and
HTMX responses. The partial SHALL render validation feedback, matching flights as
semantic `ul` and `li` content using the existing responsive flight-card classes, and
an explicit empty state.

#### Scenario: Complete page contains matching flights
- **WHEN** an ordinary valid search returns flights
- **THEN** the complete page includes the partial and renders each match once in
  semantic list and card markup

#### Scenario: Enhanced search contains matching flights
- **WHEN** an HTMX valid search returns flights
- **THEN** the partial response renders each match in the same semantic list and card
  markup used by the complete page

#### Scenario: Enhanced search is invalid
- **WHEN** an HTMX search fails `FlightSearchForm` validation
- **THEN** the partial response contains visible, announced validation feedback and no
  partially filtered flight list

#### Scenario: Enhanced search has no matches
- **WHEN** an HTMX valid search matches no flights
- **THEN** the partial response contains a visible empty-result message

### Requirement: Header-selected partial response
The flight-list view SHALL detect enhanced requests through the `HX-Request` request
header. It SHALL return only the flight-results partial when the header value is
`true`, and SHALL return the complete flight-list page for ordinary requests, while
reusing the existing `FlightSearchForm`, validation, exact filtering, and departure-time
ordering for both representations.

#### Scenario: Caller sends the HTMX header
- **WHEN** a caller sends GET `/flights/` with `HX-Request: true`
- **THEN** the response has status 200, uses the flight-results partial, and excludes
  the complete page shell and search form

#### Scenario: Caller omits the HTMX header
- **WHEN** a caller sends GET `/flights/` without `HX-Request: true`
- **THEN** the response has status 200 and uses the complete flight-list template

#### Scenario: Enhanced valid query filters flights
- **WHEN** a caller sends a valid complete query with `HX-Request: true`
- **THEN** the partial contains only exact origin, destination, and departure-date
  matches ordered by ascending departure time

### Requirement: Accessible asynchronous feedback
The search page SHALL provide a visible textual loading indicator associated with the
HTMX request and SHALL expose loading and result updates through suitable status or
live-region semantics. Feedback MUST NOT rely only on animation, and the interaction
MUST preserve visible labels, keyboard-operable controls, semantic links, and Django
validation messages.

#### Scenario: Enhanced request is in progress
- **WHEN** HTMX is loading updated flight results
- **THEN** visible loading text identifies the in-progress update and is available to
  assistive technology

#### Scenario: Updated results arrive
- **WHEN** HTMX swaps a result, validation, or empty-state response
- **THEN** the stable flight-results live-region node remains connected while its
  updated contents are exposed as a non-disruptive live update

### Requirement: No persistence or schema impact
The interaction SHALL NOT modify database models, create migrations, or change booking
and duplicate-seat behavior.

#### Scenario: Contributor checks model drift
- **WHEN** the Exercise 10 interaction is implemented and migration drift is checked
- **THEN** Django reports no model changes requiring a migration
