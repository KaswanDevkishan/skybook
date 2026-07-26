## ADDED Requirements

### Requirement: Flight results expose booking availability
Each complete-page and HTMX flight result SHALL show airline name, flight number,
route, departure and arrival times, duration, nonstop status for current direct
seeded flights, seats remaining, lowest currently available seat price, and practical
available-cabin information.

#### Scenario: Flight has varied available seats
- **WHEN** its result is rendered
- **THEN** the count excludes booked seats, the lowest price is the minimum available
  seat price, and available cabins are represented

#### Scenario: Flight has no available seats
- **WHEN** its result is rendered
- **THEN** it reports no remaining seats and does not show a Book action

### Requirement: Book actions retain selected flight identity
A result with at least one available seat SHALL provide a clear keyboard-operable
"View seats" link to that flight's booking route. The result partial MUST derive the
destination from the rendered flight rather than a generic booking URL.

#### Scenario: Visitor activates View seats
- **WHEN** a flight has one or more available seats
- **THEN** its Book link opens the booking route containing that flight's identifier

#### Scenario: HTMX replaces results
- **WHEN** an enhanced search replaces the results region
- **THEN** each remaining View seats link still identifies its own flight and works without
  requiring JavaScript

### Requirement: Flight search has a responsive travel-product presentation
The complete flight page SHALL present a hero and the existing origin, destination,
and departure-date form in an elevated search card without adding unsupported fields.
Results SHALL use route-focused cards with airline and flight identity, side-by-side
airport/time details, a visual route line, hours/minutes duration, nonstop status,
prominent lowest fare, seats remaining, and available cabins. The layout SHALL render
one card per row on mobile, two on tablet, and up to three on wide screens without
horizontal overflow.

#### Scenario: Visitor opens the complete flight page
- **WHEN** the visitor sends an ordinary GET request to the flight list
- **THEN** the page includes the search hero, three existing search fields, live
  results region, and no separate How it works explanation

#### Scenario: Visitor views a scheduled flight
- **WHEN** a flight lasts one hour and twenty-five minutes
- **THEN** its result shows `1h 25m` rather than the raw timedelta representation
