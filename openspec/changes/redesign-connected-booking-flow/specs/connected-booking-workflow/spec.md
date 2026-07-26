## ADDED Requirements

### Requirement: Booking starts from a selected flight
The system SHALL expose a flight-specific booking route and SHALL resolve the flight
from that route before offering or accepting a seat. It MUST NOT provide a generic
form that permits choosing a seat across all flights.

#### Scenario: Visitor follows a flight Book action
- **WHEN** a visitor activates Book for a flight with available seats
- **THEN** the system opens that flight's booking page and identifies the selected
  flight

#### Scenario: Visitor opens an invalid flight identifier
- **WHEN** a visitor requests the booking route for a flight that does not exist
- **THEN** the response has status 404 and no booking is created

### Requirement: Seat selection is flight-scoped
The booking form SHALL offer only seats belonging to the selected flight and SHALL
distinguish currently available and unavailable seats. Every review and confirmation
submission MUST reject a missing or unknown seat, a seat on another flight, or a seat
that is already booked.

#### Scenario: Selected flight has seats from multiple flights in the database
- **WHEN** the visitor opens its booking page
- **THEN** only that flight's seats appear as selectable controls

#### Scenario: Cross-flight seat is injected
- **WHEN** a direct submission names a valid seat belonging to another flight
- **THEN** the response shows an accessible seat error and persists no booking

#### Scenario: Booked seat is submitted
- **WHEN** a direct or stale submission names an already-booked seat
- **THEN** the response shows an accessible availability error and persists no second
  booking

### Requirement: Aircraft seat interface is data-driven and informative
The booking page SHALL render a stylized aircraft fuselage with Business before
Economy, seat-letter headings, row numbers, and aisle spacing. It SHALL derive cabin,
row, and letter placement from the selected flight's persisted seats and MUST NOT
invent selectable or unavailable seats. Each real seat presentation SHALL identify
seat number, cabin, type, formatted JPY price, and availability on hover, focus, and
through accessible text.

#### Scenario: Flight contains varied seats
- **WHEN** the visitor views seat selection
- **THEN** the aircraft map shows its real Business and Economy seats by row and letter
  with aisle cues, details, and non-color availability semantics

#### Scenario: Flight has an incomplete or expanded row
- **WHEN** persisted seats omit a position or introduce another row or letter
- **THEN** the map aligns the persisted positions without creating a form control for
  any absent seat

### Requirement: Selection summary uses non-authoritative estimates
Selecting an available native seat control SHALL progressively update a persistent
summary with seat, class, type, base fare, estimated 10% fee, and estimated total.
The server MUST recalculate all values during review and confirmation, and the
workflow MUST remain usable if the summary enhancement does not run.

#### Scenario: Visitor selects a seat
- **WHEN** the native radio selection changes with JavaScript available
- **THEN** the summary presents server-rendered estimates for that seat

#### Scenario: Script is unavailable or prices are manipulated
- **WHEN** JavaScript does not run or a client changes displayed values
- **THEN** native submission still works and server review ignores those values

### Requirement: Passenger details are validated
The workflow SHALL require a non-empty passenger name and a syntactically valid
passenger email before review or confirmation, while leaving `Booking.user` null for
this guest flow.

#### Scenario: Guest enters valid details
- **WHEN** the visitor submits a selected available seat, passenger name, and valid
  email for review
- **THEN** the server accepts the passenger details and presents the review

#### Scenario: Guest enters invalid details
- **WHEN** the visitor omits the passenger name or submits an invalid email
- **THEN** the form retains safe submitted values, displays accessible field errors,
  and creates no booking

### Requirement: Review precedes confirmation
Before persistence, the server SHALL render a review containing the selected airline
and flight number, route, departure and arrival date and time, seat number, cabin
class, seat type, base fare, taxes and fees, and total JPY price.

#### Scenario: Valid selection is reviewed
- **WHEN** a visitor submits valid seat and passenger data for review
- **THEN** all required itinerary, seat, and authoritative price details are shown and
  no booking exists yet

### Requirement: Confirmation is atomic and conflict-safe
Final confirmation MUST revalidate all untrusted identifiers and passenger data,
recalculate prices server-side, and create the guest booking within a database
transaction. The existing database-backed one-booking-per-seat constraint MUST remain
authoritative for stale or concurrent requests.

#### Scenario: Guest confirms an available seat
- **WHEN** a valid reviewed selection remains available at final confirmation
- **THEN** exactly one guest booking with immutable amounts and a reference is created
  and the response redirects to its confirmation page

#### Scenario: Two guests confirm the same seat
- **WHEN** stale or concurrent requests attempt to confirm one seat
- **THEN** at most one booking is committed and the losing request receives a visible
  availability error

#### Scenario: Confirmation is submitted without prior browser navigation
- **WHEN** a client directly submits final-confirmation fields
- **THEN** the server applies the same complete validation and either safely creates
  one valid booking or rejects the submission

### Requirement: Confirmation receipt contains booking details
The confirmation page SHALL show booking reference, passenger name and email, airline
and flight number, origin and destination, departure and arrival times, seat number,
cabin class, base fare, taxes and fees, total JPY price, and a link back to flight
search.

#### Scenario: Confirmed guest opens receipt
- **WHEN** the successful redirect resolves the created booking reference
- **THEN** the response presents all required stored booking and related itinerary
  details

#### Scenario: Unknown reference is requested
- **WHEN** a visitor requests a confirmation reference that does not exist
- **THEN** the response has status 404
