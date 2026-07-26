## Why

SkyBook's Phase 1 authentication and booking rules are already implemented and passing,
but the major-upgrade program needs an explicit, auditable baseline before the booking
workflow is restructured. The smallest safe remaining Phase 1 change is therefore a
verification-only closure that records requirement-to-test traceability and fills only
demonstrable regression-coverage gaps without altering runtime behavior.

## What Changes

- Map every Phase 1 requirement to its existing implementation and regression tests.
- Add only focused tests proven missing by that traceability review, with emphasis on
  public-booking ownership, safe pending-session contents and cleanup, local redirect
  handling, active-only booking history, cancellation inventory, and full-page/HTMX date
  parity.
- Record the accepted Phase 1 verification evidence and the invariant baseline that
  Phase 2 must preserve.
- Keep views, forms, templates, styles, models, migrations, routes, seed data, deployment
  configuration, and user-visible behavior unchanged unless verification exposes a real
  Phase 1 defect; any such defect requires the proposal to be updated before implementation.
- Preserve Django, SQLite/PostgreSQL portability, historical guest bookings and receipts,
  JPY pricing, seat-map behavior, transaction-based duplicate protection, and Render
  deployment.
- Keep the multi-step workflow, dummy payment, search expansion, airline-data changes,
  and all later roadmap phases out of scope.

## Capabilities

### New Capabilities

- `phase-1-baseline-verification`: Auditable coverage and acceptance criteria for the
  completed authentication, ownership, pending-booking, active-history, cancellation,
  navigation, hero, date-validation, and login-error baseline.

### Modified Capabilities

None. This closure adds no new product requirement and changes no existing runtime
contract.

## Impact

The planned implementation is limited to focused tests and verification documentation.
It introduces no API, dependency, runtime, database, migration, static asset, seed,
production setting, or deployment change. It is allowed within the current project scope
because it protects already authorized behavior; every later product feature remains
deferred to its own OpenSpec change.
