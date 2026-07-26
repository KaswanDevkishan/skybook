## REMOVED Requirements

### Requirement: Validated guest booking form
**Reason**: The generic all-flight seat selector permits an unsafe disconnected
journey and is replaced by flight-scoped workflow forms.

**Migration**: Enter booking through `/flights/<flight_id>/book/`; use the selected
flight's scoped seat field plus passenger details and server-side review.

### Requirement: Valid booking submission persists safely
**Reason**: Persistence now occurs only after flight-scoped review and final
confirmation rather than through the generic submission endpoint.

**Migration**: Post review and confirmation actions to the selected flight's booking
route; retain atomic creation and visible duplicate-seat handling.

### Requirement: Booking submissions are CSRF protected
**Reason**: The route-specific workflow replaces the former booking template and
submission route.

**Migration**: Every POST in the flight-specific review and confirmation workflow
remains protected by Django CSRF middleware and template tokens.

## MODIFIED Requirements

### Requirement: Accessible rendered form structure
The flight-search and flight-specific booking templates SHALL render every form
control with a visible associated label and SHALL preserve Django control IDs,
submitted values, field-level errors, and error associations. Invalid bound forms
SHALL expose an accessible validation alert without changing validation or submission
behavior.

#### Scenario: Visitor opens an unbound form
- **WHEN** a visitor opens flight search or a flight-specific booking page
- **THEN** every visible control has a visible associated label

#### Scenario: Visitor submits invalid search input
- **WHEN** a visitor submits an invalid flight search
- **THEN** the bound form retains values, renders existing field errors, and exposes
  validation feedback with alert semantics

#### Scenario: Visitor submits invalid booking input
- **WHEN** a visitor submits invalid passenger data or an invalid, cross-flight, or
  unavailable seat
- **THEN** the bound workflow retains safe values, creates no booking, renders field
  errors, and exposes validation feedback with alert semantics

## ADDED Requirements

### Requirement: Flight-scoped booking form validation
The booking form SHALL receive the selected flight as server-owned context and SHALL
limit its seat queryset and cleaning to that flight. Review and confirmation actions
MUST validate seat ownership and current availability even when browser controls are
bypassed.

#### Scenario: Form is constructed for a flight
- **WHEN** seats for multiple flights exist
- **THEN** its selectable queryset contains only unbooked seats from the supplied
  flight

#### Scenario: Tampered identifier is posted
- **WHEN** a submitted seat is outside the scoped queryset
- **THEN** Django form validation rejects it before persistence

### Requirement: New booking POSTs are CSRF protected
Every workflow-changing booking request SHALL use POST and include Django's CSRF token,
and endpoints MUST reject requests without a valid token when CSRF checks are
enforced.

#### Scenario: Workflow form is rendered
- **WHEN** the visitor opens seat selection or price review
- **THEN** each POST form contains a CSRF token

#### Scenario: Token is missing
- **WHEN** a CSRF-enforcing client submits review or confirmation without a valid token
- **THEN** Django returns status 403 and creates no booking

