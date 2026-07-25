## Context

SkyBook is a small Flask 3 course project whose current runtime surface is an
application factory, two smoke-test routes, and a WSGI entry point. Contributor
guidance already establishes many correct guardrails, but README structure examples,
exercise status, package metadata, and OpenSpec context are inconsistent or incomplete.
The locally installed skills support proposing, applying, updating, syncing, exploring,
and archiving OpenSpec changes.

## Goals / Non-Goals

**Goals:**

- Establish one consistent description of the Flask architecture, course phase,
  domain intent, tooling, commands, and repository layout.
- Give future agents durable OpenSpec and Exercise 4 scope constraints.
- Confirm that documented commands match `pyproject.toml` and CI.
- Strengthen exclusions for local state and credentials without ignoring source files.

**Non-Goals:**

- Changing application code, runtime behavior, or dependencies.
- Adding Django or any second web framework.
- Implementing models, persistence, flight search, booking, authentication, or UI.

## Decisions

1. Treat checked-in files and executable configuration as the source of truth. Update
   documentation to describe the real `app/__init__.py`, current files, and configured
   commands rather than creating planned directories or a lockfile to match stale text.
   The alternative—adding placeholder implementation structure—would violate Exercise 4.
2. Put concise contributor rules in `AGENTS.md`, onboarding and project overview in
   `README.md`, machine-consumed project constraints in `openspec/config.yaml`, and
   package/tool settings in `pyproject.toml`. This avoids making any one document serve
   incompatible audiences.
3. Preserve the existing `uv` commands and CI sequence unless verification proves them
   invalid. No new tooling or dependency is warranted for a documentation audit.
4. Express exclusions in `.gitignore` with narrow patterns for environments, caches,
   coverage output, secrets, and SQLite files. Avoid broad patterns that could hide
   intentional fixtures or documentation.
5. Validate with Ruff formatting checks, Ruff linting, Pytest with coverage, OpenSpec
   validation, and targeted repository searches for stale Django or feature claims.

## Risks / Trade-offs

- Documentation can drift again → Anchor commands to `pyproject.toml` and CI and keep
  planned structure clearly labeled.
- Credential ignore patterns can create false confidence → State that secrets must
  never be committed; ignore rules are only a safety net.
- Exercise labels may change later → Keep the Exercise 4 restriction explicit now and
  revise it through a future OpenSpec change when the course advances.
- Existing local tools may reformat unrelated files → Use check-only commands during
  verification and limit edits to approved documentation/configuration files.
