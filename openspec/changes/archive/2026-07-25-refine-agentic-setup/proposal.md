## Why

SkyBook's contributor and agent guidance has drifted from the repository: the README
contains stale paths and exercise status, project metadata is incomplete, and OpenSpec
has no project-specific context. Refining these materials now will keep future work
aligned with the course scope and prevent framework or feature creep.

## What Changes

- Reconcile `AGENTS.md` and `README.md` with the actual repository structure, commands,
  installed OpenSpec skills, and Exercise 4 boundaries.
- Make the Python 3.12, Flask 3, SQLite, `uv`, Ruff, Pytest, and coverage conventions
  consistent across contributor-facing documentation and configuration.
- Add OpenSpec context that requires agents to preserve Flask, consult specifications,
  and avoid implementing deferred application features during Exercise 4.
- Improve project metadata and Git exclusions where the audit identifies safe,
  documentation- or configuration-only gaps.
- Verify the documented setup, formatting, linting, and testing commands.
- Do not add Django, database models, flight search, booking, authentication, or the
  seat-map interface.

## Capabilities

### New Capabilities

- `repository-agent-guidance`: Defines consistent project guidance, tooling commands,
  course-scope guardrails, OpenSpec workflow expectations, and repository hygiene.

### Modified Capabilities

None.

## Impact

Changes are limited to documentation, metadata, OpenSpec configuration and artifacts,
and Git exclusion rules. Application code, runtime behavior, APIs, dependencies, and
database schema remain unchanged.
