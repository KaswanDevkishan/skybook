## ADDED Requirements

### Requirement: Authentication and ownership scope is documented
Repository guidance SHALL identify Django-native registration, sign in, POST sign out,
account-aware navigation, owned booking history, authenticated booking association,
editable passenger prefill, and status-based future owned-booking cancellation as
permitted current work. It SHALL require authentication before price review and new
booking completion, preserve historical guest bookings and receipts, and keep refunds,
guest lookup, payment redesign, flight tracking, external APIs, and custom password
storage out of scope. It SHALL state that passenger email need not belong to an account
and account existence is never disclosed through passenger-email validation.

#### Scenario: Agent reviews account milestone guidance
- **WHEN** an agent reads repository instructions before account implementation
- **THEN** it can identify the permitted authentication and ownership work, preserved
  historical guest and booking invariants, passenger-email privacy, and explicitly
  deferred features

### Requirement: Authentication security and verification remain documented
Contributor guidance SHALL require Django password hashing and validators, session
authentication, CSRF protection, safe redirect validation, owner-filtered booking access,
POST logout, credential hygiene, and regression verification for SQLite and Render
PostgreSQL settings.

#### Scenario: Contributor prepares authentication work
- **WHEN** a contributor consults the README and repository guidance
- **THEN** the documented workflow prevents manual password handling, unsafe redirects,
  cross-user booking exposure, GET logout, and committed credentials
