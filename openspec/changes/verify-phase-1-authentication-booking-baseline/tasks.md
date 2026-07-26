## 1. Build Phase 1 traceability

- [x] 1.1 Map each Phase 1 requirement group to its responsible form, view, service,
  query, model, template, style, URL, and existing automated tests.
- [x] 1.2 Review the mapping for uncovered security and preservation boundaries,
  specifically anonymous creation, session allowlisting and cleanup, safe redirects,
  passenger-email non-disclosure, ownership, receipt visibility, cancellation
  idempotence, released inventory, and historical guest compatibility.
- [x] 1.3 Record the accepted baseline and identify which invariants the Phase 2 OpenSpec
  change must preserve.

## 2. Close only demonstrated test gaps

- [x] 2.1 Reuse existing equivalent tests and list any normative Phase 1 scenario that
  has no automated coverage.
- [x] 2.2 Add the smallest focused regression test for each demonstrated gap without
  changing application code, templates, styles, routes, settings, seed data, or models.
- [x] 2.3 If any test or inspection exposes a runtime defect, stop implementation and
  revise the proposal, design, affected specifications, and tasks before applying a fix.

## 3. Verify and hand off the baseline

- [x] 3.1 Run `uv run ruff format --check .` and `uv run ruff check .`.
- [x] 3.2 Run `uv run pytest` and confirm the configured coverage report does not regress.
- [x] 3.3 Run `uv run python manage.py check` and
  `uv run python manage.py makemigrations --check --dry-run`.
- [x] 3.4 Strictly validate this OpenSpec change and run `git diff --check`.
- [x] 3.5 Review the resulting file list and explicitly confirm that no application
  implementation, migration, dependency, seed, production configuration, commit, push,
  archive, merge, or deployment occurred.
