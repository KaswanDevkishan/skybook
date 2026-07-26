## Why

Exercise 11 requires SkyBook to move from a development-only Django setup to a
reproducible, secure Render deployment while keeping the existing local workflow and
application behavior intact. This work is allowed for Exercise 11 and establishes the
minimum production infrastructure needed to operate the course project from GitHub's
`main` branch.

## What Changes

- Add locked production dependencies for Gunicorn, WhiteNoise, PostgreSQL, and
  `DATABASE_URL` configuration.
- Make security-sensitive Django settings environment-driven, with safe production
  behavior and convenient SQLite-based local defaults.
- Add Render infrastructure configuration for a web service and PostgreSQL database,
  including locked installation, static collection, migration, health checking, and a
  Gunicorn start command bound to Render's `PORT`.
- Serve collected static assets through WhiteNoise without committing generated output.
- Add focused production-settings tests and deployment verification commands.
- Document Render provisioning, environment variables, migrations, superuser creation,
  static and future media storage, troubleshooting, and rollback.
- Keep authentication screens, payments, checkout, workers, file uploads, external
  airline APIs, unrelated interface changes, and the complete booking workflow as
  non-goals. Docker, Redis, and Celery are not introduced.

## Capabilities

### New Capabilities

- `render-production-deployment`: Defines the secure, repeatable Render web-service,
  PostgreSQL, Gunicorn, WhiteNoise, deployment, verification, and operational
  documentation contract.

### Modified Capabilities

- `django-project-foundation`: Extends the development-only SQLite foundation with
  environment-selected PostgreSQL production configuration while retaining SQLite
  when `DATABASE_URL` is absent.
- `repository-agent-guidance`: Advances repository guidance to Exercise 11 and adds the
  production deployment, secret-handling, generated-static, and ephemeral-media scope
  boundaries.

## Impact

The change affects `pyproject.toml`, `uv.lock`, Django settings, static-file storage and
middleware, a new `render.yaml`, production configuration tests, `.gitignore`, and
`README.md`. Runtime integrations are Render Web Services and Render PostgreSQL; the
public application routes, health endpoint, domain schema, existing migrations,
booking invariants, and local SQLite workflow remain compatible.
