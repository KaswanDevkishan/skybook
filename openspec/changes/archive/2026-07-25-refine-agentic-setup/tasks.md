## 1. Reconcile Contributor Documentation

- [x] 1.1 Update `README.md` to match the real repository tree, correct
  `app/__init__.py`, remove or label nonexistent files and directories as planned, and
  state the Exercise 4 documentation/configuration-only scope.
- [x] 1.2 Review `AGENTS.md` against the specification and remove any ambiguity about
  Flask-only architecture, OpenSpec-first work, installed skill workflow, deferred
  features, future domain constraints, commands, and repository hygiene.
- [x] 1.3 Cross-check `README.md` and `AGENTS.md` so Python 3.12, Flask 3, SQLite, `uv`,
  Ruff, Pytest, coverage, guest/registered bookings, and server-side duplicate-seat
  prevention are described consistently as current tooling or planned behavior.

## 2. Refine Project Configuration

- [x] 2.1 Replace the placeholder package description in `pyproject.toml` without
  changing runtime or development dependencies.
- [x] 2.2 Add concise SkyBook project context and artifact rules to
  `openspec/config.yaml`, including Flask preservation, relevant-spec review, Exercise
  4 boundaries, and the prohibition on application-feature implementation.
- [x] 2.3 Audit `.gitignore` and add only missing, targeted exclusions for tokens,
  passwords, environment files, virtual environments, caches, coverage output, and
  local database files.

## 3. Verify the Agentic Setup

- [x] 3.1 Confirm the locally installed OpenSpec skills cover the documented propose,
  explore, apply, update, sync, and archive workflow without adding framework-specific
  assumptions.
- [x] 3.2 Run `uv run ruff format --check .`, `uv run ruff check .`, and
  `uv run pytest`; resolve documentation/configuration issues only and leave
  application code unchanged.
- [x] 3.3 Search contributor guidance and configuration for stale paths, unsupported
  Django assumptions, or claims that deferred features already exist.
- [x] 3.4 Validate the `refine-agentic-setup` change with OpenSpec and inspect the final
  diff to confirm only documentation and configuration changed.
