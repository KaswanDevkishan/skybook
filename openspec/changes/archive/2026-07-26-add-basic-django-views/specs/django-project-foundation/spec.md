## MODIFIED Requirements

### Requirement: Deferred product features
The initial Django project SHALL provide only its foundation, administrative model
access, reservation schema, tests, and the explicitly bounded basic home, flight-list,
flight-detail, placeholder booking, and health views. It SHALL NOT provide flight
search or filtering, a seat-map interface, authentication pages, payment features,
booking persistence through the placeholder form, or a complete booking workflow.

#### Scenario: Initial application scope is reviewed
- **WHEN** a contributor inspects the routes, templates, and application services
- **THEN** the application contains only the permitted foundation, schema,
  administration, test behavior, and basic HTTP views

#### Scenario: Visitor submits the placeholder booking form
- **WHEN** valid passenger placeholder data is submitted
- **THEN** the application redirects without selecting a flight or seat and without
  creating a booking
