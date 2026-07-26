## Context

The working tree contains the completed Phase 1 authentication and booking-ownership
implementation under `add-user-authentication-booking-ownership`. Its active OpenSpec
tasks are 83/83 complete, strict validation succeeds, and the full suite currently passes
154 tests with 94% coverage. Code inspection confirms the required root redirect, flight
hero, local-date validation, sign-in error presentation, authentication gate, pending
resume, passenger-email independence, owned booking creation, active account list,
status-based cancellation, and historical guest compatibility.

The next roadmap phase will restructure the booking journey. Before that work begins,
Phase 1 needs a concise acceptance baseline that distinguishes existing verified
behavior from new Phase 2 behavior. Existing working-tree changes belong to the user and
must not be reformatted, refactored, archived, committed, or otherwise disturbed by this
closure.

## Goals / Non-Goals

**Goals:**

- Produce a requirement-to-code-and-test traceability review for every Phase 1 behavior.
- Add a focused regression test only when a concrete normative scenario lacks equivalent
  coverage.
- Re-run the complete quality gates and record an accepted baseline for Phase 2.
- Keep the database-backed Confirmed-seat uniqueness rule and owner assignment invariant
  explicit in the verification evidence.

**Non-Goals:**

- Changing forms, views, URLs, templates, styles, services, models, migrations, seed data,
  settings, or deployment configuration.
- Reworking the existing authentication or cancellation design.
- Adding the multi-step journey, dummy payment, new search inputs, real airline demo data,
  or any later roadmap feature.
- Committing, pushing, archiving, merging, or deploying the existing working tree.

## Decisions

### Treat Phase 1 as implemented and make closure verification-only

The audit found no failing behavior or incomplete requirement, so the change will not
manufacture a product modification merely to create implementation work. A verification
change is safer than reopening cross-cutting authentication and booking code immediately
before Phase 2.

The alternative was to fold Phase 1 closure into the Phase 2 workflow change. That would
blur the accepted baseline and make regressions harder to attribute.

### Use scenario traceability before adding tests

Each Phase 1 requirement will be mapped to the responsible code path and at least one
test scenario. Existing equivalent tests count; duplicate tests will not be added for
checkbox completeness. A new test is justified only when it proves a missing security,
authorization, state, response-mode, or data-preservation boundary.

The alternative was a broad rewrite of current tests. That would create noise, risk
coverage regression, and exceed the smallest safe scope.

### Do not change schema or runtime code inside this proposal

No migration is needed because the required nullable historical ownership, booking
status, immutable prices, and Confirmed-only seat constraint already exist. If later
verification uncovers a real runtime defect, work stops and the proposal, design, specs,
and task scope must be revised and revalidated before any fix is applied.

### Use the repository's standard gates as acceptance evidence

Acceptance requires the full Pytest suite with coverage, Ruff formatting and lint checks,
Django system checks, migration drift detection, strict OpenSpec validation, and
`git diff --check`. The final review must confirm no application implementation or
migration entered this verification-only change.

## Risks / Trade-offs

- **Existing tests can give false confidence through duplicated assertions.** → Build the
  traceability matrix from normative scenarios and inspect responsible code paths before
  deciding coverage is sufficient.
- **A verification task may discover a real defect.** → Stop, update the planning
  artifacts to describe the defect and runtime impact, then seek review before applying
  a fix.
- **The dirty working tree makes attribution difficult.** → Restrict this change's edits
  to its OpenSpec artifacts, roadmap documentation, and any subsequently justified
  focused tests; review file lists and diffs explicitly.
- **A no-runtime-change proposal can become unnecessary test churn.** → Prefer references
  to existing tests and add nothing when coverage is already equivalent.

