## ADDED Requirements

### Requirement: Phase 1 behavior has auditable traceability
The verification record SHALL map every Phase 1 requirement group to the responsible
runtime path and one or more equivalent automated tests. The mapping SHALL cover root
navigation, hero simplification, local-date validation, login error presentation,
authentication gating, pending-booking resume, passenger-email non-disclosure, booking
ownership, active-only My Bookings, cancellation, and preservation of historical guest
bookings.

#### Scenario: Reviewer audits the Phase 1 baseline
- **WHEN** the Phase 1 verification record is reviewed
- **THEN** every required behavior is linked to its implementation location and automated
  regression evidence

### Requirement: Verification fills only demonstrated coverage gaps
The verification change MUST reuse existing equivalent tests and SHALL add a focused
test only when traceability demonstrates that a normative Phase 1 scenario lacks
automated coverage. Any added test MUST preserve the current user-visible contract and
MUST NOT require unrelated refactoring.

#### Scenario: Existing coverage proves a requirement
- **WHEN** an existing test already exercises the normative behavior and its security or
  data boundary
- **THEN** the verification record references that test without adding a duplicate

#### Scenario: A concrete coverage gap is found
- **WHEN** no existing test exercises a normative Phase 1 behavior
- **THEN** a focused regression test is planned for only that missing behavior

### Requirement: Runtime and schema remain unchanged during baseline closure
The Phase 1 verification closure SHALL NOT change application runtime code, templates,
styles, routes, settings, dependencies, seed data, database models, or migrations. If
verification discovers a runtime defect, implementation MUST pause until the OpenSpec
proposal and affected behavioral specifications are revised and strictly validated.

#### Scenario: Verification completes without a defect
- **WHEN** traceability and quality gates confirm the existing Phase 1 contract
- **THEN** no application implementation or migration is produced

#### Scenario: Verification exposes a runtime defect
- **WHEN** a required Phase 1 scenario fails or is contradicted by code inspection
- **THEN** the verification change stops before a fix and its planning scope is revised

### Requirement: Phase 1 passes the repository quality gates
The accepted baseline MUST pass the full Pytest suite with configured coverage, Ruff
format and lint checks, Django system checks, migration drift detection, strict OpenSpec
validation, and `git diff --check`. The final evidence SHALL explicitly confirm that no
commit, push, archive, merge, or deployment occurred.

#### Scenario: Phase 1 baseline is accepted
- **WHEN** all traceability and quality checks complete successfully
- **THEN** the verification record identifies the passing commands and confirms the
  repository remained uncommitted, unpushed, unarchived, unmerged, and undeployed
