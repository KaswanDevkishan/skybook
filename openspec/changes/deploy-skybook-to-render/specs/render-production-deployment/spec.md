## ADDED Requirements

### Requirement: Locked production runtime
SkyBook SHALL declare and lock Gunicorn, WhiteNoise, a Python 3.12-compatible
PostgreSQL driver, and any database-URL parser used by production configuration.

#### Scenario: Production dependencies are installed
- **WHEN** Render installs the project from the committed lockfile
- **THEN** the environment contains the application server, static middleware,
  PostgreSQL driver, and database URL support needed to start SkyBook

### Requirement: Safe environment-driven Django configuration
SkyBook SHALL read `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, and
`CSRF_TRUSTED_ORIGINS` from documented environment variables, SHALL default `DEBUG` to
false, SHALL require an environment-provided secret key on Render, and SHALL retain
convenient non-secret localhost defaults outside Render.

#### Scenario: Production settings are complete
- **WHEN** Django loads on Render with all required environment variables
- **THEN** debug mode is disabled and the configured secret, hosts, and trusted HTTPS
  origins are applied

#### Scenario: Production secret is absent
- **WHEN** Django loads in the Render environment without `SECRET_KEY`
- **THEN** configuration fails without using a source-controlled production secret

#### Scenario: Debug environment variable is absent
- **WHEN** Django loads without an explicit `DEBUG` value
- **THEN** debug mode is false

#### Scenario: Contributor uses local defaults
- **WHEN** Django loads outside Render without production environment variables
- **THEN** local management and development remain possible with documented localhost
  and development-only defaults

### Requirement: Environment-selected production database
SkyBook SHALL configure PostgreSQL from `DATABASE_URL` when it is supplied and SHALL
use the existing SQLite database configuration when it is absent.

#### Scenario: Render supplies its database connection
- **WHEN** `DATABASE_URL` contains the Render PostgreSQL connection URL
- **THEN** Django selects the PostgreSQL backend using that connection

#### Scenario: Contributor has no database URL
- **WHEN** a contributor runs Django locally without `DATABASE_URL`
- **THEN** Django uses the existing local SQLite database

### Requirement: WhiteNoise static asset delivery
SkyBook SHALL place WhiteNoise immediately after Django `SecurityMiddleware`, define
`STATIC_URL` and `STATIC_ROOT`, collect static assets during the production build, and
use WhiteNoise compressed manifest storage on Render without committing collected
output.

#### Scenario: Production static assets are built
- **WHEN** the Render build runs `collectstatic --noinput`
- **THEN** versioned compressed static assets are written beneath `STATIC_ROOT` for
  WhiteNoise to serve

#### Scenario: Middleware order is inspected
- **WHEN** Django loads the middleware configuration
- **THEN** WhiteNoise follows `SecurityMiddleware` before application middleware

#### Scenario: Repository contents are inspected
- **WHEN** collected static output exists locally after verification
- **THEN** Git ignore rules prevent that generated output from being committed

### Requirement: Secure Render proxy operation
When running on Render with debug mode disabled, SkyBook SHALL honor Render's forwarded
HTTPS protocol, redirect insecure requests, use secure session and CSRF cookies, and
retain Django host and CSRF-origin validation.

#### Scenario: HTTPS request crosses the Render proxy
- **WHEN** Render forwards a request with its HTTPS protocol header
- **THEN** Django recognizes the request as secure without redirecting it repeatedly

#### Scenario: Production security configuration is checked
- **WHEN** `manage.py check --deploy` runs with production-like environment variables
- **THEN** the project does not suppress security checks by enabling debug mode,
  wildcard hosts, or disabled CSRF protection

### Requirement: Reproducible Render service lifecycle
The repository SHALL describe a Render web service deployed from GitHub `main`, using
a locked dependency and static build, a distinct safe migration step, Gunicorn with
`skybook.wsgi:application` bound to Render's `PORT`, Render PostgreSQL, and `/health/`
as its health check.

#### Scenario: Render builds a revision
- **WHEN** a selected `main` revision is deployed
- **THEN** Render installs the frozen production dependency set and successfully
  collects static assets

#### Scenario: Render releases a revision
- **WHEN** the build has succeeded
- **THEN** existing Django migrations run against PostgreSQL before the new web process
  receives traffic

#### Scenario: Render starts the web service
- **WHEN** Render provides `PORT` and executes the configured start command
- **THEN** Gunicorn imports `skybook.wsgi:application` and listens on that port without
  using Django's development server

#### Scenario: Render checks application health
- **WHEN** Render requests `/health/`
- **THEN** the preserved health endpoint returns its successful plain-text response

### Requirement: Deployment verification coverage
SkyBook SHALL include automated tests for production settings and static configuration,
and its documented release verification SHALL cover tests, formatting, linting,
normal and deployment Django checks, migration drift, static collection, Gunicorn WSGI
import, and strict OpenSpec validation.

#### Scenario: Contributor verifies the release candidate
- **WHEN** the documented verification sequence is run with production-like variables
- **THEN** all existing tests and focused production tests pass and each configured
  deployment boundary completes successfully

### Requirement: Render operations documentation
Contributor documentation SHALL explain the production architecture, Render and GitHub
setup, required environment variables, exact build and start commands, migrations,
superuser creation, static delivery, future media storage, deployment verification,
troubleshooting, and rollback without exposing credentials.

#### Scenario: Operator follows the deployment guide
- **WHEN** an operator provisions SkyBook from the documented `main` branch workflow
- **THEN** they can configure, build, migrate, start, verify, troubleshoot, and roll
  back the service without placing a secret in source control

#### Scenario: Future media uploads are considered
- **WHEN** a contributor plans uploaded-media support
- **THEN** the documentation directs them to persistent object storage rather than
  Render's ephemeral app-local filesystem

### Requirement: Exercise 11 scope remains focused
The production deployment SHALL NOT add Docker, Redis, Celery, workers, file-upload
functionality, payments, external airline APIs, unrelated interface changes, or schema
changes not genuinely required by deployment.

#### Scenario: Deployment diff is reviewed
- **WHEN** a reviewer inspects the Exercise 11 implementation
- **THEN** it contains deployment configuration and verification without the deferred
  infrastructure, product features, or unrelated schema and interface changes
