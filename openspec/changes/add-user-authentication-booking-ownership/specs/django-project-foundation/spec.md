## ADDED Requirements

### Requirement: Authentication milestone remains Django-native
The current product milestone SHALL permit built-in Django registration, session
authentication, account pages, nullable booking ownership, and status-based owned
booking cancellation while retaining Django as the sole web framework. It MUST NOT
introduce custom password storage or require a custom user model for this change.
Authentication SHALL be required to review and complete new public bookings, while
historical null-user bookings and their receipts remain supported.

#### Scenario: Contributor implements account support
- **WHEN** authentication and booking ownership are added
- **THEN** the implementation uses Django's built-in authentication user, hashing,
  validators, sessions, CSRF protection, and existing project structure

### Requirement: Authentication preserves database portability
Account and booking-ownership behavior SHALL work with SQLite development and PostgreSQL
on Render and SHALL preserve the existing database-backed one-booking-per-seat invariant.
A reservation schema migration MUST safely default historical bookings to Confirmed and
enforce one Confirmed booking per seat while allowing retained Cancelled history.

#### Scenario: Contributor checks migration state
- **WHEN** the nullable booking user relationship already represents the planned schema
- **THEN** Django reports no reservation model drift and no no-op migration is created
