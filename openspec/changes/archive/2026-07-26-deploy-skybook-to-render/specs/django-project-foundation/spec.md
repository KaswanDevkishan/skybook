## MODIFIED Requirements

### Requirement: SQLite development database
The Django configuration SHALL use SQLite when `DATABASE_URL` is absent, SHALL use the
database described by `DATABASE_URL` when it is supplied for production, and SHALL keep
local database files and database credentials out of version control.

#### Scenario: Clean development database is initialized
- **WHEN** a contributor applies migrations without overriding database configuration
- **THEN** Django creates or updates a local SQLite database

#### Scenario: Production database is initialized
- **WHEN** deployment applies the existing migrations with Render's PostgreSQL
  `DATABASE_URL`
- **THEN** Django creates or updates the production PostgreSQL schema without requiring
  a new application schema migration
