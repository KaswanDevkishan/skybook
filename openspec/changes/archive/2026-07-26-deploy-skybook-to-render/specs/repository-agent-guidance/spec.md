## MODIFIED Requirements

### Requirement: Current exercise scope boundary
Repository guidance SHALL identify the current work as Exercise 11 and SHALL permit the
Render deployment foundation: Gunicorn, Render PostgreSQL with a SQLite development
fallback, WhiteNoise static delivery, environment-based production configuration,
deployment tests, infrastructure configuration, and operational documentation. It
SHALL preserve the existing Django foundation, schema, administration, public views,
validated GET flight search, POST guest booking creation, semantic responsive
interface, and server-driven HTMX interaction. It SHALL continue to prohibit
authentication screens, payments, an interactive seat-map interface, checkout,
external airline APIs, unrelated interface changes, other client-side frameworks,
Docker unless genuinely required, Redis, Celery, workers, file uploads, and a complete
booking workflow. It SHALL direct contributors not to add seat class or another schema
field unless a later requirement genuinely requires it.

#### Scenario: Exercise 11 deployment work is requested
- **WHEN** an agent prepares the specified Render production deployment
- **THEN** repository guidance identifies the focused production configuration,
  dependencies, tests, and documentation as permitted within Exercise 11

#### Scenario: Exercise 10 HTMX feature is requested
- **WHEN** an agent prepares or maintains the specified server-driven flight-result
  update
- **THEN** repository guidance identifies that focused interaction as preserved and
  permitted within Exercise 11

#### Scenario: Existing search or booking work is reviewed
- **WHEN** an agent changes the presentation or response representation of flight search
- **THEN** repository guidance requires the existing validation, GET fallback,
  persistence, and database-backed duplicate-seat behavior to remain intact

#### Scenario: Existing application behavior is reviewed
- **WHEN** an agent changes settings, dependencies, static handling, or deployment
  configuration
- **THEN** repository guidance requires current routes, validation, persistence,
  migrations, and database-backed duplicate-seat behavior to remain intact

#### Scenario: Deferred feature is requested
- **WHEN** a requested task would add a prohibited infrastructure component, product
  feature, schema change, or unrelated interface change
- **THEN** the guidance identifies that work as outside the Exercise 11 scope

### Requirement: Repository hygiene
Guidance and Git exclusions SHALL cover tokens, passwords, Render credentials,
`SECRET_KEY`, `DATABASE_URL`, `.env` files, virtual environments, caches, coverage
artifacts, collected static output, and local SQLite/database files, while making clear
that ignore patterns do not authorize storing secrets. Guidance SHALL also state that
Render's app-local filesystem is ephemeral and is not suitable for future persistent
uploaded media.

#### Scenario: Local development creates generated or sensitive files
- **WHEN** standard local environment, cache, coverage, secret, database, or collected
  static files appear
- **THEN** Git excludes them and contributor guidance says they must not be committed

#### Scenario: Contributor plans persistent media
- **WHEN** future application work requires user-uploaded files
- **THEN** repository guidance requires persistent object storage instead of relying on
  the web service filesystem
