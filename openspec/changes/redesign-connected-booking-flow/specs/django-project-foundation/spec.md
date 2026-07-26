## MODIFIED Requirements

### Requirement: Deferred product features
The Django course project SHALL provide its existing foundation, administration,
validated flight search, semantic responsive interface, HTMX result replacement, and
Render deployment while adding the explicitly authorized flight-specific guest
booking flow, classified and priced seats, immutable booking prices, review, and
confirmation, plus the explicitly authorized progressive aircraft-style seat map. It
SHALL NOT provide accounts, payment gateway, booking dashboard or lookup,
cancellation, round trips, tracking, external airline APIs, copied airline branding,
or unrelated infrastructure and redesign work.

#### Scenario: Authorized booking milestone is reviewed
- **WHEN** a contributor inspects routes, models, forms, templates, and services
- **THEN** the application contains the connected guest workflow and required pricing
  schema without any excluded later features

#### Scenario: Visitor confirms a booking
- **WHEN** valid guest and flight-scoped seat data passes review and final validation
- **THEN** one booking is persisted without starting payment or authentication

#### Scenario: Existing deployment behavior is reviewed
- **WHEN** the new migration and flow run locally or on Render
- **THEN** SQLite fallback, PostgreSQL selection, static delivery, health checks, and
  production security remain supported
