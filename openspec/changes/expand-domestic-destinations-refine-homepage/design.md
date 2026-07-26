## Context

The active connected-booking redesign already gives seeded flights classified, priced
seats and relies on the database for booking integrity. The current command defines
four broad city codes and five flights, keys flights by airline and flight number,
computes a future schedule only for `get_or_create` defaults, and updates seat
attributes by flight and seat number. Render invokes this command after migrations.

This change crosses seed definitions, preservation behavior, search choices, shared
presentation, tests, README, and OpenSpec guidance, but requires no schema migration or
new dependency. Existing rows may include the current `TYO`, `OSA`, `SPK`, and `FUK`
identities, arbitrary user-created cities and flights, already-booked seats, and seeded
flights whose original future dates are now past.

## Goals / Non-Goals

**Goals:**

- Represent approximately 30–40 major airport-served Japanese destinations across all
  requested regions with stable unique codes and clear English names.
- Provide a curated route and flight set large enough for meaningful origin and
  destination selection.
- Preserve every existing row, identifier, schedule, seat identity, and booking across
  first and repeated runs.
- Apply the existing cabin, seat-type, and whole-yen pricing structure to every newly
  seeded flight without duplicates.
- Install the supplied homepage copy, remove the site footer, and preserve compact,
  accessible navigation and the connected search-to-booking journey.

**Non-Goals:**

- A complete airport directory, every possible route, live or externally synchronized
  schedules, round trips, or operational aviation accuracy.
- Renaming or consolidating existing broad city records, updating old seeded schedules,
  repricing booked seats, or modifying bookings.
- Authentication navigation, accounts, payments, unrelated page redesign, a new
  framework, or deployment infrastructure changes.

## Decisions

### Preserve legacy identities and add airport-code identities

The seed catalog will retain the existing four code/name pairs exactly and add stable
IATA-style airport codes with clear English airport-served destination names until the
catalog totals approximately 30–40 entries. Codes are declared once and validated for
uniqueness before database writes. `get_or_create(code=..., defaults={"name": ...})`
continues to avoid renaming any existing row, even if its display name differs.

This deliberately allows broad legacy codes and airport-specific additions to coexist.
Replacing `TYO`, `OSA`, `SPK`, or `FUK` with airport codes would either change
identifiers or strand existing flight relationships, while keying by name would be
less stable.

### Curate a regional network with immutable seeded flight identities

The flight catalog will use a bounded set of realistic direct demonstrations joining
regional hubs and selected cross-regional destinations. Every requested region will
appear in at least one valid origin or destination relationship. Each definition keeps
a stable airline/flight-number identity and supplies origin code, destination code,
day offset, local departure clock, and plausible positive duration.

The command validates unique flight identities, known destination codes, distinct
endpoints, and positive durations before writing. It then retains the current
`get_or_create` pattern in which calculated datetimes appear only in `defaults`.
Consequently a missing flight receives a schedule relative to the run date, while an
existing seeded flight is never rescheduled—even after its date passes.

Generating all route pairs was rejected because it would create noisy, unrealistic
demo volume and weaken stable test expectations.

### Create seats only for flights created or owned by the seed catalog

Every flight resolved from the stable seed catalog receives the established Economy
and Business seat template with Window/Middle/Aisle classification and Decimal-
compatible whole-yen prices. Seat identity remains `(flight, seat_number)`.
Idempotent creation fills missing seats without duplicating them.

Existing seat rows, especially booked seats, must not be repriced or reclassified by
routine repeated seeding. Creation defaults therefore apply to missing seats; the
command does not treat the seed catalog as authority to rewrite persisted seat data.
This is safer than `update_or_create`, which can silently mutate the price snapshot
source for an existing or booked seat.

### Prove preservation with before-and-after snapshots

Tests will snapshot existing city primary keys and attributes, flight endpoints and
datetimes, seat identities and prices, and booking fields before a later-date repeated
run. Assertions will verify that only missing catalog records are added and all
snapshotted values remain unchanged. Separate tests cover catalog size and uniqueness,
route validity and region coverage, first-run future schedules, repeated counts, and
seat structure/pricing on newly created flights.

This is stronger than count-only idempotency tests, which can miss destructive
replacement or in-place mutation.

### Remove the shared footer without replacing its landmark

The footer element is removed from the base template and footer-only CSS and assertions
are deleted. The skip link, header, primary navigation, one main landmark, heading
structure, focus behavior, and responsive layout remain. The exact supplied copy
replaces only the homepage hero text. SkyBook remains linked to `/`, and Flights remains
the sole navigation item with the existing current-page behavior.

A visually hidden or empty footer was rejected because the requirement is absence, not
restyling. Account links remain deferred because they would advertise unavailable
behavior.

### Document demonstration scope explicitly

README will describe the catalog as a representative set of major domestic Japanese
airports or airport-served destinations and the flights as curated demonstration data,
not a complete or live aviation schedule. It will also retain seeding, search, booking,
and Render execution guidance.

## Risks / Trade-offs

- [Legacy metropolitan codes coexist with airport codes] → Preserve them explicitly,
  explain the demonstration scope, and never rename referenced rows.
- [A future edit introduces duplicate or dangling catalog data] → Validate codes,
  flight identities, endpoint membership, distinct endpoints, and duration before the
  atomic command writes.
- [Repeated seeding mutates schedules or booked-seat pricing] → Use creation defaults
  only and verify full before/after snapshots with an advanced mocked run date.
- [More flights make the default unfiltered result page longer] → Keep the network
  curated and rely on the existing validated full-page and HTMX filters.
- [Route realism becomes stale] → Describe the data as illustrative and avoid claims
  of live service frequency or completeness.
- [Footer removal weakens structure] → Retain all useful header, navigation, main,
  skip-link, heading, focus, and responsive semantics; update the explicit landmark
  contract and tests.

## Migration Plan

1. Update seed catalog definitions and preflight validation without changing models.
2. Make destination, flight, and seat creation additive and preservation-safe.
3. Update the homepage/base templates and remove footer-only styles and tests.
4. Add seed preservation, route, pricing, interface, search, and booking regressions;
   update README and active OpenSpec artifacts.
5. Run formatting, linting, tests, Django checks, migration-drift detection, strict
   OpenSpec validation, and whitespace validation.
6. Deploy through the existing Render sequence; the idempotent command adds only
   missing catalog rows.

Rollback restores the previous application files but does not delete newly added demo
rows. If demo rows ever require removal, that must be a separately reviewed,
reference-aware data operation; bookings and existing schedules must never be deleted
as part of rollback.

## Open Questions

None. The catalog size is intentionally approximate, the network intentionally curated,
and authentication navigation remains a separate change.
