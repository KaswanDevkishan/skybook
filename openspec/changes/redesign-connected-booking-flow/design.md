## Context

SkyBook currently has one Django form that exposes every available `Seat`, creates a
guest `Booking` in one POST, and redirects home. Search results already have a reusable
HTMX partial, bookings already rely on a database uniqueness constraint and a
transactional conflict path, demo data is seeded during Render builds, and settings
select SQLite locally or PostgreSQL from `DATABASE_URL`.

This change crosses models, migrations, query annotations, forms, views, URLs,
templates, styles, seed data, tests, and documentation. Existing rows may predate
prices and classifications, and production migrations must be safe on PostgreSQL as
well as SQLite. The current repository guidance describes the full booking workflow as
deferred; this explicitly authorized later milestone updates that boundary.

## Goals / Non-Goals

**Goals:**

- Connect flight search to a flight-specific seat, passenger, review, confirmation,
  and receipt journey.
- Make seat classification and JPY pricing explicit and make confirmed booking totals
  immutable.
- Enforce flight ownership, current availability, authoritative pricing, and
  duplicate-seat safety on the server at every relevant submission.
- Preserve full-page and HTMX search, guest booking, SQLite development, and Render
  PostgreSQL deployment.
- Deliver an accessible responsive aircraft-style seat map as a progressive visual
  layer over the existing native, server-validated seat controls.

**Non-Goals:**

- Accounts, authentication UI, a bookings dashboard, lookup, cancellation, round
  trips, payment processing, or payment data.
- Copied airline layouts or branding, model-backed aircraft geometry, destination
  imagery, tracking, or external airline APIs.
- Docker, Redis, Celery, workers, file uploads, another web framework, or broad visual
  redesign.

## Decisions

### Use model enums and whole-yen DecimalFields

`Seat` will define Django `TextChoices` for cabin class (`ECONOMY`, `BUSINESS`) and
seat type (`WINDOW`, `MIDDLE`, `AISLE`). `price` and all booking amount fields will be
`DecimalField`s with zero decimal places because JPY amounts are represented in whole
yen, while calculations continue to use `Decimal`.

Alternatives considered: free-form strings permit invalid values; floats introduce
binary rounding; integer fields obscure that values are monetary. Enums plus decimal
fields make the domain and validation explicit.

### Backfill in stages before enforcing final constraints

The migration will first add safely nullable/defaulted fields, run a deterministic
data migration, and then enforce final non-null/unique definitions. Existing seats
receive Economy, a seat type inferred from the final seat letter where conventional
(`A`/`F` window, `B`/`E` middle, other letters aisle), and a documented fallback fare
of JPY 15,000. Existing bookings receive snapshots computed from that migrated fare,
an existing-row creation timestamp, and a collision-checked reference.

Alternatives considered: a single static default cannot safely populate a unique
reference and cannot classify seats sensibly; deleting/reseeding would violate data
preservation.

### Persist only confirmed bookings

The review step does not create a database booking. The final confirmation POST
revalidates the flight, seat, availability, and passenger form, recalculates all
amounts, and atomically creates a confirmed booking. Because every persisted booking
is confirmed and cancellation is out of scope, no status column is introduced in this
change.

Alternatives considered: persisting pending bookings complicates seat availability,
expiry, cleanup, and background work; a status field with only one reachable state
adds no useful invariant.

### Use one flight-scoped endpoint with explicit workflow actions

A named route under `/flights/<flight_id>/book/` handles the seat/passenger and review
states, and the final successful POST redirects (Post/Redirect/Get) to a named
confirmation route containing the booking reference. Form action values distinguish
review from confirmation. The form queryset is always scoped to unbooked seats on the
URL's flight. The confirmation route resolves by opaque reference rather than exposing
a generic booking editor.

Selected identifiers and passenger fields may be carried as normal or hidden form
values between steps, but are treated as untrusted. No submitted price is used.

Alternatives considered: several temporary database models or session state add
cleanup and state-sync complexity; client-only multi-step JavaScript violates
progressive enhancement.

### Apply a single server-side 10% fee rule

Taxes and fees equal 10% of the selected seat's base fare, rounded to the nearest
whole yen using `Decimal` and `ROUND_HALF_UP`; total price is base fare plus the
rounded fee. A focused pricing function is the only calculation source used by
review, confirmation, migration backfill, and tests. Templates only format supplied
amounts and never calculate them.

Alternatives considered: hard-coded per-template arithmetic risks inconsistent totals;
multiple fee components would add domain detail not requested for this academic flow.

### Generate random readable references under a unique constraint

References use an uppercase `SKY-` prefix followed by a short alphabet that omits
ambiguous characters. A cryptographically secure generator produces candidates, the
database unique constraint is authoritative, and creation retries a bounded number of
reference collisions inside transaction savepoints. Seat uniqueness failures are
reported as availability conflicts rather than reference retries.

Alternatives considered: sequential primary keys disclose volume and are less
user-friendly; UUIDs are unnecessarily long for a classroom confirmation code.

### Compute flight availability from the database

The flight result queryset will annotate available-seat count and lowest available
price and prefetch or aggregate available cabin values without per-result queries.
Duration is derived from arrival minus departure, and seeded flights are labelled
nonstop because the model contains no leg structure. The same context powers full-page
and HTMX partial responses. A Book link is rendered only when the available count is
positive.

Alternatives considered: template-side counting creates N+1 queries and can count
booked seats incorrectly; adding stopover schema is out of scope.

### Render semantic native seat controls

Available seats use labelled native radio controls grouped first by cabin and then row.
Each label includes seat number, type, price, and availability text. Unavailable seats
remain visible for orientation but are disabled and explicitly named unavailable.
CSS supplies layout, state, and `:focus-visible`; color is supplementary. Minimal
vanilla JavaScript may improve step presentation but cannot be required to book.

### Layer an aircraft map over real seat data

The view parses supported seat numbers with an anchored digits-plus-letters pattern,
groups them by cabin and numeric row, and derives each cabin's letter headings from
the seats that actually exist for the selected flight. Missing positions render only
as inert alignment space, never as invented or selectable seats. Adjacent aisle-type
seats can introduce a visual aisle without encoding one flight's fixed column count
in the template.

The template renders a CSS-drawn nose, fuselage, and subtle wings around semantic
Business-first and Economy-second cabin sections. Every real seat remains a native
radio and associated label. Hover and focus expose the same number, class, type, JPY
fare, and availability available to assistive technology. Booked seats remain disabled
and visible. This intentionally avoids copied airline branding and aircraft SVG.

An external vanilla script listens for native radio changes and updates a persistent
sidebar summary from server-rendered data attributes. The estimated 10% fee and total
are produced by the shared Python pricing function before rendering. The script
performs no booking validation and submits no prices; without it, selection, review,
confirmation, stale-seat rejection, and receipt all continue through normal forms.

Desktop uses a left map and sticky right details/summary column. At tablet widths the
sidebar follows the map. On mobile, only the map region scrolls horizontally and a
sticky bottom review action remains touch-friendly, preventing whole-page overflow.

### Refine search presentation without changing its contract

The complete flight page will place the existing three-field GET form in an elevated
search card within a navy travel-product hero. The reusable results partial will use
route-focused cards with formatted hours/minutes duration, prominent minimum fare,
availability and cabin summaries, and a flight-specific "View seats" link only when
availability is positive. CSS will explicitly provide one, two, and three-column
result layouts at mobile, tablet, and wide breakpoints. The result region finishes the
page without an additional explanatory section or unnecessary trailing spacing. The
flight page uses a stable 72rem maximum content width, with matching hero gutters, and
does not use transform scaling, zoom, or reduced root font sizing.

Alternatives considered: adding passenger, cabin, or round-trip controls would imply
unsupported search behavior; client-side duration formatting would weaken progressive
enhancement; an additional explanatory section would duplicate the connected flow
already communicated by the search and results.

### Use the brand as the sole homepage navigation link

The shared header keeps the SkyBook brand as a normal keyboard-operable link to `/`
and removes the redundant Home navigation item. Flights remains the only primary
navigation item and retains `aria-current="page"` across flight search, detail, and
booking routes. The compact navigation must preserve visible focus behavior, semantic
navigation markup, touch-friendly sizing, and responsive layout.

No Sign in item—functional, disabled, or placeholder—is added. Authentication and its
navigation affordances are deferred to a separate future OpenSpec change so this
change does not imply or simulate account behavior.

Alternatives considered: retaining both the brand and Home duplicates the same
destination; adding a disabled Sign in item advertises behavior outside this change.

## Risks / Trade-offs

- [Existing data has no historical fare] → Backfill a clearly documented JPY 15,000
  base and matching 10% fee; never pretend a later seeded price was historical.
- [A seat becomes booked between review and confirm] → Recheck inside `transaction.atomic`
  and retain the database unique constraint; return an accessible conflict error.
- [Booking-reference collision handling masks a seat conflict] → Isolate candidate
  inserts with savepoints and distinguish the violated constraint or recheck seat
  occupancy before retrying only a reference collision.
- [Availability annotations become database-specific] → Use Django ORM expressions
  and aggregate filters covered on SQLite, avoiding PostgreSQL-only SQL.
- [Confirmation references are discoverable] → Use high-entropy random references;
  this page is a receipt, not the future authenticated dashboard or guest-lookup
  feature, and no search endpoint is added.
- [Removal of generic routes breaks old bookmarks/tests] → Update named route
  contracts, navigation, tests, and README together; missing legacy URLs return 404
  rather than exposing an unsafe fallback.
- [Irregular seat numbers could break visual alignment] → Parse with a strict anchored
  pattern, retain safe fallback labels, and never create a control without a database
  seat.

## Migration Plan

1. Add model fields in a staged schema/data migration and backfill every existing row.
2. Apply final non-null and unique constraints, retaining the existing one-booking-per-
   seat constraint.
3. Update seed logic, domain services, queries, views, URLs, templates, and docs.
4. Verify migration from the prior schema on SQLite and test PostgreSQL-compatible
   settings and ORM behavior; run the full requested quality and strict OpenSpec suite.
5. Deploy through the existing Render build sequence, which migrates before running
   the idempotent seed command.

Rollback of application code must remain paired with schema compatibility. Before
production data uses the new fields, the migration can be reversed normally; after
new bookings exist, rollback should restore the previous application revision without
dropping the new columns, or first export data and use an explicit forward migration.
No rollback may delete bookings.

## Open Questions

None. The first iteration intentionally fixes the fee rule at 10%, persists only
confirmed bookings, and defers all payment and account behavior.
