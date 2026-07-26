## 1. Production Dependencies

- [x] 1.1 Add Gunicorn, WhiteNoise, Psycopg 3 binary, and `dj-database-url` production
  dependencies to `pyproject.toml` with Python 3.12-compatible constraints.
- [x] 1.2 Regenerate `uv.lock` with `uv` and verify the frozen production dependency
  set installs successfully without introducing another web framework.

## 2. Environment and Database Settings

- [x] 2.1 Add focused environment parsing for `DEBUG`, Render detection,
  comma-separated `ALLOWED_HOSTS`, and comma-separated `CSRF_TRUSTED_ORIGINS`, with
  safe defaults and documented localhost convenience.
- [x] 2.2 Require an environment-provided `SECRET_KEY` on Render while retaining only a
  clearly development-only fallback outside the production environment.
- [x] 2.3 Parse `DATABASE_URL` into a PostgreSQL Django configuration when supplied and
  preserve the existing SQLite configuration when absent.
- [x] 2.4 Configure `SECURE_PROXY_SSL_HEADER`, HTTPS redirect, secure session cookies,
  and secure CSRF cookies for non-debug Render operation without weakening host or CSRF
  validation.
- [x] 2.5 Fail Render configuration when neither its external hostname nor non-empty
  explicit host and trusted-origin values are available.

## 3. Static Files and Production Server

- [x] 3.1 Add WhiteNoise immediately after `SecurityMiddleware`, define `STATIC_URL`
  and `STATIC_ROOT`, and select compressed manifest static-file storage on Render.
- [x] 3.2 Update `.gitignore` to exclude collected static output and confirm no secrets,
  environment files, local databases, credentials, or generated deployment artifacts
  are tracked.
- [x] 3.3 Verify Gunicorn imports `skybook.wsgi:application` and document/configure a
  production start command that binds `0.0.0.0:$PORT` without using `runserver`.

## 4. Render Blueprint

- [x] 4.1 Add `render.yaml` for a GitHub `main`-branch Python web service and managed
  PostgreSQL database, wiring `DATABASE_URL` from the database and leaving secret
  values generated or dashboard-managed.
- [x] 4.2 Pin Python 3.12.8 and configure one fail-fast free-tier build command that
  installs frozen production dependencies, migrates, and runs `collectstatic
  --noinput`, with Gunicorn as the start command and `/health/` as the health-check
  path.
- [x] 4.3 Review the Blueprint and deployment diff to confirm existing migrations,
  schema, public routes, health behavior, and duplicate-seat protection remain
  unchanged.

## 5. Automated Coverage

- [x] 5.1 Add settings tests covering the false `DEBUG` default, environment overrides,
  strict Render `SECRET_KEY` handling, host/origin list parsing, and localhost
  development defaults.
- [x] 5.2 Add database settings tests covering the SQLite fallback and PostgreSQL
  selection from a representative non-secret `DATABASE_URL`.
- [x] 5.3 Add static and security tests covering WhiteNoise middleware order,
  `STATIC_ROOT`, Render manifest storage, proxy SSL configuration, HTTPS redirect, and
  secure cookies.
- [x] 5.4 Add or update deployment configuration tests covering the locked build,
  free plan, build-time migration and static collection, absent `preDeployCommand`,
  pinned Python runtime, Gunicorn `PORT` binding, database wiring, branch, and
  preserved health-check path.

## 6. Operations Documentation and Guidance

- [x] 6.1 Update `README.md` with the Exercise 11 architecture, GitHub/Render setup,
  required environment variables, and exact build and start commands, referencing
  GitHub issues #23, #24, and #25 where appropriate.
- [x] 6.2 Document safe migration and `createsuperuser` commands, static collection and
  WhiteNoise delivery, free-tier PostgreSQL expiry and Shell limitations, paid-tier
  pre-deploy guidance, and the requirement for persistent object storage if uploaded
  media is added later.
- [x] 6.3 Document deployment verification, common configuration/build/database/static
  troubleshooting, logs and health checks, and code/database rollback precautions.
- [x] 6.4 Update repository agent guidance from Exercise 10 to Exercise 11, preserving
  all existing application boundaries and adding production secret, generated-static,
  and ephemeral-filesystem rules.

## 7. Verification and Release Readiness

- [x] 7.1 Run `uv run ruff format .` and `uv run ruff check .`.
- [x] 7.2 Run `uv run pytest` and confirm all existing and new tests pass without
  reducing coverage.
- [x] 7.3 Run `uv run python manage.py check` and
  `uv run python manage.py makemigrations --check --dry-run`, confirming no deployment
  schema change is generated.
- [x] 7.4 With production-like non-secret environment values, run
  `uv run python manage.py check --deploy` and address actionable security warnings
  without disabling Django protections.
- [x] 7.5 Run `uv run python manage.py collectstatic --noinput` and a Gunicorn
  configuration/import smoke test for `skybook.wsgi:application`.
- [x] 7.6 Run strict OpenSpec validation for `deploy-skybook-to-render` and inspect the
  final Git diff for credentials, collected output, lockfile drift, and unrelated
  changes.
- [x] 7.7 After human review, push the approved revision to GitHub `main`, apply the
  Render Blueprint with authorized account access, and verify the build, migration,
  `/health/`, static assets, application pages, and logs before declaring deployment
  complete.

## 8. Production Data Initialization

- [x] 8.1 Add a safe, idempotent `seed_demo_data` management command with stable
  identifiers, connected future flights, and seats, without deleting bookings or
  changing the schema.
- [x] 8.2 Run the command between migration and static collection in the fail-fast
  Render build.
- [x] 8.3 Add focused tests for empty-database population, idempotency, preserved
  existing data, flight-search cities and results, and booking-form seats.
- [x] 8.4 Document automatic course-demonstration seeding and local command usage,
  while distinguishing controlled real-production data loading.
- [x] 8.5 Run the requested Pytest, Django, Ruff, strict OpenSpec, and diff checks.
- [x] 8.6 Verify the live PostgreSQL database contains seeded cities, airlines, future
  flights, and seats, and confirm the seeded cities, flight results, and seats appear
  in the public search and booking forms.

## 9. Live Deployment Verification

- [x] 9.1 On 2026-07-26, verify the Render Blueprint deployment at
  `https://skybook-33ks.onrender.com` completed successfully with PostgreSQL connected,
  migrations and demo-data initialization running during deployment, Gunicorn serving
  the application, WhiteNoise-delivered CSS, successful flight search and booking-form
  population, and a successful `/health/` response.
