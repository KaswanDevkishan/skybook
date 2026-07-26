# SkyBook Major Upgrade Roadmap

## Purpose and delivery rules

This roadmap evolves SkyBook into a polished Japanese domestic airline-booking
demonstration while preserving Django 5.2, Python 3.12, JPY pricing, SQLite development,
Render PostgreSQL, Django templates, vanilla HTML/CSS/JavaScript, and the existing HTMX
progressive enhancement.

Each numbered phase is an independent OpenSpec change and should normally be delivered
as one focused pull request. A phase may be split into the explicitly recommended PR
boundaries below when review risk warrants it, but its OpenSpec change remains the
single source of truth. Every phase must preserve historical bookings, authoritative
server-side pricing and inventory, authentication ownership, cancellation history,
SQLite/PostgreSQL portability, accessibility, and ordinary non-HTMX behavior.

The following remain global non-goals unless a later approved change explicitly says
otherwise: Flask or another web framework, real payments or refunds, live airline or
flight-status APIs, airline logos or copied branding, round trips, Redis, Celery,
workers, Docker, file uploads, destructive historical-data rewrites, or secrets in Git.

## Current baseline and Phase 1 assessment

The working tree already implements the Phase 1 runtime behavior under the active
`add-user-authentication-booking-ownership` OpenSpec change. Its 83 tasks are complete,
it validates strictly, and the complete test suite passes (154 tests, 94% coverage).

| Phase 1 area | Assessment | Repository evidence |
| --- | --- | --- |
| Root navigation | Complete | `/` redirects to the named flight list; the shared brand links there; the old home template is removed. |
| Hero simplification | Complete | The flight page keeps only the required heading above the search card; obsolete hero copy is absent. |
| Date validation | Complete | Dynamic local-date `min`, server validation, exact message, today/future acceptance, and full-page/HTMX tests exist. |
| Login errors | Complete | One friendly `role="alert"` message is rendered; raw non-field errors are not duplicated; field errors remain associated. |
| Authentication gate | Complete | Anonymous visitors can submit seat/passenger input only into a pending session and cannot reach review or creation. |
| Pending resume | Complete | Only flight, seat, passenger name, and email are stored; resumed data is revalidated and repriced; safe redirects are tested. |
| Passenger email | Complete | Passenger identity remains editable and independent of account identity; non-disclosure tests exist. |
| Booking ownership | Complete | Public confirmation passes `request.user`; owner-scoped receipts and historical guest receipts are preserved. |
| My Bookings | Complete | The account query includes only owned Confirmed rows and renders the exact active-booking empty state and flight action. |
| Cancellation | Complete | Owner-only GET confirmation and CSRF POST status transition, future-only rule, idempotence, inventory release, and no-refund notice are tested. |
| Verification | Functionally complete; closure remains | The suite covers the listed behavior. The smallest safe remaining work is a verification-only baseline closure with no runtime or schema change. |

Phase 1 should not be redesigned before Phase 2. Its remaining proposal is
`verify-phase-1-authentication-booking-baseline`, limited to explicit traceability,
regression-test gap review, and final quality-gate evidence.

## Dependency order

The recommended primary order is:

`1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14`

The strict technical dependencies are:

- Phase 2 depends on the authenticated ownership and pending-session baseline in Phase 1.
- Phase 3 depends on the multi-step state machine in Phase 2.
- Phase 4 depends on authoritative cabin inventory and prices, but can start after Phase 3.
- Phase 5 depends on Phase 4's airline filter contract and must precede airline-rich
  booking-management displays.
- Phase 6 depends on Phases 3 and 5.
- Phases 7, 8, and 9 depend on the owner-only booking detail established in Phase 6.
- Phase 10 depends on the airline/flight presentation vocabulary from Phase 5.
- Phase 11 depends on Phase 4 cabin/passenger availability semantics and must preserve
  the Phase 3 booking transaction.
- Phase 12 should follow the finalized models from Phases 5, 10, and 11.
- Phase 13 audits all earlier public and owner-only endpoints, so it follows Phases 7–12.
- Phase 14 is final integration polish and follows every user-facing phase.

Phases 7, 8, and 9 may be developed in parallel after Phase 6 if they remain separate
changes and PRs. Phase 10 may proceed in parallel with Phases 7–9 after Phase 5. Phase 11
should merge before Phase 12 and before final accessibility polish.

## Phase plans

### Phase 1 — Close authentication and booking-rule baseline

**Goal:** Record and protect the already implemented authentication, ownership, search-date,
active-booking, and cancellation baseline without changing runtime behavior.

**Dependencies:** Existing authentication/ownership and connected-booking changes.

**Database:** No new migration. Retain nullable ownership for historical guest rows and
the Confirmed-only seat uniqueness constraint.

**Security:** Verify anonymous creation is impossible, pending sessions contain only
allowlisted values, redirects stay local, receipts remain owner-scoped, and cancellation
is owner-only POST.

**Deployment:** No Render configuration change. Run the full SQLite suite and retain
PostgreSQL-compatible constraints/settings tests.

**Recommended PR boundary:** One verification-only PR containing focused missing
regression tests and traceability documentation, if review finds any actual gap.

**GitHub issue:** `Phase 1: Verify authentication and booking-rule baseline`

### Phase 2 — Introduce the five-step booking workflow

**Goal:** Separate Choose seat, Review selection, Passenger details, Dummy payment, and
Confirmation into explicit server-driven states with a visible progress indicator and
safe back navigation.

**Dependencies:** Phase 1.

**Database:** Prefer no migration; store transient workflow state in the server-side
session. Add a schema field only if idempotent finalization cannot be expressed safely
with the existing unique booking reference and seat constraint.

**Security:** Allowlist session fields, reject workflow bypass and cross-flight
injection, revalidate the selected seat at every sensitive boundary, and never trust
hidden prices.

**Deployment:** Confirm session and transaction behavior on SQLite and PostgreSQL; no
new service dependency.

**Recommended PR boundary:** One PR for the workflow state machine, views/templates,
progress component, and regression tests. Do not include payment validation beyond the
minimal placeholder needed to connect Phase 3.

**GitHub issue:** `Phase 2: Build the server-driven five-step booking journey`

### Phase 3 — Add dummy payment and idempotent final confirmation

**Goal:** Add the demo-only card form, prominent no-charge notice, and create exactly one
owned booking only after successful simulated payment confirmation.

**Dependencies:** Phase 2.

**Database:** Likely no migration. If replay protection requires persisted workflow
tokens, use a minimal non-sensitive, unique idempotency record with expiration rules;
prefer the existing booking reference/transaction when sufficient.

**Security:** Never persist, log, query-string encode, analyze, or session-store card
number or CVV. Recheck inventory and price inside the final transaction.

**Deployment:** No payment provider, credentials, webhook, or new infrastructure.
Ensure secure POST handling works behind Render's HTTPS proxy.

**Recommended PR boundary:** One PR for demo form validation, finalization idempotency,
race handling, and non-persistence tests.

**GitHub issue:** `Phase 3: Add secure simulated payment and idempotent confirmation`

### Phase 4 — Improve airport search, cabin search, sorting, and filters

**Goal:** Add progressively enhanced accessible airport autocomplete, passenger count,
cabin selection, sorting, and filters while preserving normal GET and HTMX responses.

**Dependencies:** Phase 3; existing cabin/price inventory.

**Database:** No required migration for basic query fields. Add indexes only after query
measurement demonstrates a need; any index migration must be portable.

**Security:** Treat every browser value as untrusted, cap passenger count, validate
airport identity and route difference, and calculate cabin availability server-side.

**Deployment:** Measure query counts and PostgreSQL plans for compound filters; keep
SQLite behavior deterministic and avoid a search service.

**Recommended PR boundaries:** (1) airport autocomplete and added search fields;
(2) sorting/filtering and performance tests.

**GitHub issue group:** `Phase 4A: Accessible airport autocomplete and search inputs`;
`Phase 4B: Flight sorting, filters, and cabin availability correctness`

### Phase 5 — Add real Japanese airline names as neutral demo data

**Goal:** Introduce verified operating Japan-based passenger carriers, stable codes,
carrier types, neutral badges, airline filtering, and the required non-affiliation/demo
disclaimer without implying partnership.

**Dependencies:** Phase 4 airline filter contract.

**Database:** Expected migration for airline IATA code and carrier type, with nullable or
safe defaults for existing fictional carriers. Use additive data migration/seeding;
never rewrite historical flights or bookings.

**Security:** No special authorization change. Avoid remote logo dependencies, scraped
assets, or untrusted airline content.

**Deployment:** Verify current carrier facts from official sources at implementation
time; keep seeded schedules explicitly simulated and idempotent on Render.

**Recommended PR boundaries:** (1) carrier schema and non-destructive seed transition;
(2) filter/display/disclaimer and documentation.

**GitHub issue group:** `Phase 5A: Model and seed neutral Japanese carrier demo data`;
`Phase 5B: Add carrier filters, badges, and non-affiliation notices`

### Phase 6 — Expand booking management

**Goal:** Add active booking cards, a canonical owner-only detail page, receipt download
and print views, calendar entry point, status labels, and consistent cancellation links.

**Dependencies:** Phases 3 and 5.

**Database:** Usually no migration because immutable booking snapshots and status exist.
Add fields only for genuinely missing receipt facts; do not derive ownership from email.

**Security:** Centralize owner-only lookup for registered bookings, preserve historical
guest receipt behavior, block cross-user enumeration, and keep cancellation POST-only.

**Deployment:** Downloads must stream safely without durable filesystem writes.

**Recommended PR boundaries:** (1) canonical detail/list authorization and UI;
(2) print/download receipt endpoints.

**GitHub issue group:** `Phase 6A: Add owner-only booking details and active cards`;
`Phase 6B: Add print-friendly and downloadable receipts`

### Phase 7 — Add a demonstration digital boarding pass

**Goal:** Provide a responsive, printable SkyBook boarding pass with a non-travel
disclaimer and a QR code containing only a booking reference or owner-only URL.

**Dependencies:** Phase 6.

**Database:** Expected migration only if gate and boarding time must be stored rather
than safely derived; avoid duplicating passenger secrets.

**Security:** Owner-only access, non-sensitive QR payload, no third-party QR service,
and no airline trademark artwork.

**Deployment:** Use a pinned local QR library or a small server-generated implementation;
verify static/print output on Render without filesystem persistence.

**Recommended PR boundary:** One PR for data contract, QR generation, page, print CSS,
authorization, and tests.

**GitHub issue:** `Phase 7: Add an owner-only demonstration boarding pass`

### Phase 8 — Add owner-only ICS calendar downloads

**Goal:** Generate safe timezone-aware `.ics` files for confirmed owned bookings.

**Dependencies:** Phase 6; Phase 7 if shared gate/terminal fields are persisted there.

**Database:** No migration unless Phase 7 did not supply required terminal/gate fields.

**Security:** Owner-only lookup, escaped ICS fields, safe content-disposition filenames,
no active download for Cancelled bookings, and no unrelated personal data.

**Deployment:** Generate responses in memory; test Asia/Tokyo behavior under production
timezone settings.

**Recommended PR boundary:** One PR for ICS serializer, endpoint, authorization, and
format/timezone tests.

**GitHub issue:** `Phase 8: Add secure booking calendar downloads`

### Phase 9 — Send booking confirmation email

**Goal:** Send a non-blocking confirmation email after successful creation using
Django's email framework.

**Dependencies:** Phases 3 and 6.

**Database:** No migration required. An optional delivery-attempt model is deferred
unless operational requirements later justify it.

**Security:** Environment-only credentials, non-sensitive failure logs, owner-safe
receipt links, and no payment values.

**Deployment:** Console backend locally, locmem in tests, environment-configured backend
on Render. Booking commits even when delivery fails.

**Recommended PR boundary:** One PR for settings, message construction, post-commit send
behavior, documentation, and outbox/failure tests.

**GitHub issue:** `Phase 9: Send non-blocking booking confirmation emails`

### Phase 10 — Add simulated flight status

**Goal:** Provide a flight-number search and a clearly simulated status page using local
timestamps plus stored override states.

**Dependencies:** Phase 5.

**Database:** Expected migration for explicit operational override status and optional
gate/terminal fields. Preserve existing schedules and use safe defaults.

**Security:** Public read-only data only; validate search input and avoid claims of live
accuracy or external APIs.

**Deployment:** Timezone-aware deterministic calculations; no polling service or worker.
HTMX polling, if used, must remain optional and bounded.

**Recommended PR boundaries:** (1) status model/domain calculation;
(2) search page, route progress UI, and tests.

**GitHub issue group:** `Phase 10A: Model deterministic simulated flight status`;
`Phase 10B: Build the simulated flight-status experience`

### Phase 11 — Expand aircraft layouts and seat attributes

**Goal:** Seed realistic six-abreast cabin layouts with extra-legroom and exit-row
attributes, richer pricing, accessible tooltips, and mobile-contained scrolling.

**Dependencies:** Phase 4; preserve Phase 3 finalization.

**Database:** Expected additive migration for aircraft/layout identity and seat
attributes such as extra legroom and exit row. Never mutate booked seat identity or
historical booking snapshots.

**Security:** Server-authoritative inventory and price; reject injected or stale seat
identifiers and retain native form controls.

**Deployment:** Idempotent additive seeding must be safe on existing Render databases;
larger seat volumes require query-count and response-size tests.

**Recommended PR boundaries:** (1) schema and preservation-safe seed expansion;
(2) accessible seat-map rendering and responsive behavior.

**GitHub issue group:** `Phase 11A: Add preservation-safe aircraft and seat attributes`;
`Phase 11B: Render realistic accessible aircraft seat layouts`

### Phase 12 — Improve Django Admin

**Goal:** Add safe search, filters, date hierarchies, readonly snapshots, availability
counts, and related-object links for reservation data and users.

**Dependencies:** Phases 5, 10, and 11.

**Database:** No expected migration; admin configuration should use existing schema.

**Security:** Staff-only Django Admin, escaped links, readonly immutable pricing, safe
querysets, and no destructive booking bulk actions. Validate any status update action.

**Deployment:** Avoid N+1 queries and expensive unbounded annotations in list views.

**Recommended PR boundary:** One PR, with admin tests separated by model inside the same
change.

**GitHub issue:** `Phase 12: Add safe and efficient Django Admin workflows`

### Phase 13 — Harden security

**Goal:** Audit authentication, authorization, requests, booking transactions, data
handling, production settings, dependencies, and add password reset/session policy plus
approved lightweight rate limiting if justified.

**Dependencies:** Phases 7–12 and all resulting public/owner-only endpoints.

**Database:** Possible migration only for a lightweight rate-limit/audit store if the
selected Django-compatible approach requires it. Password reset uses Django primitives.

**Security:** This phase owns the threat model, endpoint authorization matrix, CSRF and
method audit, redirect safety, idempotency, logging review, secret scanning, dependency
review, and account-enumeration resistance.

**Deployment:** Verify `DEBUG=false`, hosts, proxy SSL, secure cookies, CSRF origins,
secret requirements, and Render health/start/build behavior. Do not add Redis without
separate approval.

**Recommended PR boundaries:** (1) threat model and endpoint/settings hardening;
(2) password reset/session policy; (3) lightweight login rate limiting, only if approved.

**GitHub issue group:** `Phase 13A: Audit authorization, requests, booking, and production security`;
`Phase 13B: Add Django-native password reset and session policy`;
`Phase 13C: Evaluate and add lightweight login rate limiting`

### Phase 14 — Complete UI, responsive, and accessibility polish

**Goal:** Unify the full experience with responsive navigation, consistent feedback,
loading/empty states, accessible errors and seat states, premium navy styling, and no
clipping or page-level overflow.

**Dependencies:** All previous phases.

**Database:** No migration expected.

**Security:** Preserve server validation, CSRF, safe messages, and non-disclosing error
copy while changing presentation.

**Deployment:** Verify collected static assets, WhiteNoise manifests, content size, and
representative mobile/desktop pages in production-like settings.

**Recommended PR boundaries:** (1) design-system tokens/components and navigation;
(2) booking/account/status responsive polish; (3) accessibility regression pass.

**GitHub issue group:** `Phase 14A: Consolidate SkyBook UI components and navigation`;
`Phase 14B: Polish responsive booking and account experiences`;
`Phase 14C: Complete accessibility and overflow regression pass`

## Migration forecast

| Phase | Expected migration |
| --- | --- |
| 1 | None |
| 2 | None preferred |
| 3 | None preferred; possible minimal idempotency model only if required |
| 4 | None; optional measured indexes |
| 5 | Airline IATA/carrier-type fields and additive data transition |
| 6 | None expected |
| 7 | Optional boarding/gate fields |
| 8 | None expected |
| 9 | None expected |
| 10 | Flight status override and optional gate/terminal fields |
| 11 | Aircraft/layout and seat-attribute fields plus additive data migration |
| 12 | None |
| 13 | None preferred; possible approved rate-limit store |
| 14 | None |

Every migration-bearing phase must include migration-executor preservation tests,
SQLite/PostgreSQL-compatible operations, idempotent seed tests where relevant, and
explicit proof that historical bookings, flight schedules, seat identity, and immutable
price snapshots are not destructively rewritten.

## Cross-phase quality gates

Each phase must run formatting and lint checks, the full Pytest/coverage suite, Django
system checks, migration drift detection, strict validation of its OpenSpec change, and
`git diff --check`. Deployment-sensitive phases must also run static collection,
production-setting tests, Gunicorn import checks, and appropriate `check --deploy`
configuration checks. UI phases require keyboard, screen-reader semantics, responsive
layout, no-JavaScript/progressive-enhancement, full-page/HTMX parity where applicable,
and no page-level horizontal overflow.

## Major program risks

- Workflow state fragmentation or browser replay could create bypasses or duplicate
  bookings; keep one server-owned state machine and idempotent transactional finalization.
- Payment-shaped inputs create disproportionate privacy risk even in a demo; never
  persist or log them and keep the no-charge notice explicit.
- Airline names can imply affiliation; verify facts from official sources, use neutral
  text only, and display the disclaimer consistently.
- Additive seed changes can accidentally mutate production demo history; snapshot and
  preservation tests are mandatory before every seed/schema expansion.
- SQLite and PostgreSQL differ in locking and conditional constraints; concurrency and
  migration behavior must be tested and reviewed for both.
- Owner-only derivative artifacts (receipt, boarding pass, ICS) expand the authorization
  surface; centralize booking lookup and test cross-user/anonymous access for each route.
- Email and rate-limiting dependencies can introduce operational failure modes; keep
  booking success independent of email and avoid infrastructure additions without need.
- Late UI changes can regress semantics and progressive enhancement; Phase 14 must refine
  shared components without weakening server validation or native controls.
