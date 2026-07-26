# SkyBook

SkyBook is a simple airline ticket reservation system for a Web Engineering course.
Exercise 11 prepares the Django application for Render, and the first major booking
redesign connects flight search to seat selection, passenger details, authoritative
JPY price review, confirmation, and a booking receipt. Existing HTMX search and the
semantic responsive interface remain intact. SQLite is used locally; production uses
Render PostgreSQL.

The current milestone provides:

- A generated Django project and `reservations` application
- `City`, `Airline`, `Flight`, `Seat`, and `Booking` models
- Django's built-in authentication user model for registered bookings
- Guest bookings through a nullable `Booking.user`
- Database constraints for valid routes, times, scheduled flights, seats, and bookings
- Django admin registration, migrations, model tests, and coverage
- Home, searchable flight-list, flight-detail, connected guest-booking, confirmation,
  and health views
- GET-based flight search with validated city and departure-date input
- Flight-scoped, CSRF-protected guest booking with validated seat and passenger input
- Economy and Business seats with Window, Middle, and Aisle types and varied JPY prices
- Immutable booking-time price snapshots and unique `SKY-XXXXXXXX` references
- Semantic page landmarks, skip navigation, logical headings, and accessible form
  feedback
- A namespaced external stylesheet with responsive layouts and visible focus states
- A pinned HTMX 2.0.4 dependency and server-rendered flight-result updates
- Progressive-enhancement fallback to the existing complete-page GET search
- A Render Web Service running Gunicorn with PostgreSQL and WhiteNoise static delivery
- Idempotent course-demonstration data initialization during Render deployment

Authentication screens, real payments, aircraft-shaped SVG seat maps, booking
dashboards, cancellation, guest lookup, round trips, tracking, destination galleries,
external airline APIs, and unrelated infrastructure remain deferred. Confirmation is
a simulated academic checkout and never collects card data.

## Project Structure

```text
skybook/
├── manage.py
├── skybook/                  # Django project settings, URLs, ASGI, and WSGI
├── reservations/             # Main domain application
│   ├── migrations/
│   ├── static/reservations/
│   ├── templates/reservations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── tests/                    # Pytest model, constraint, URL, and view tests
├── openspec/                 # Specifications and active changes
├── pyproject.toml            # Dependencies and quality-tool configuration
├── uv.lock                   # Locked dependency versions
├── render.yaml               # Render web-service and PostgreSQL Blueprint
├── AGENTS.md                 # Repository guidance for coding agents
└── .github/workflows/ci.yml
```

## Data Model

| Model | Purpose and relationships |
| --- | --- |
| `City` | Named location with a unique normalized code |
| `Airline` | Named carrier with a unique normalized code |
| `Flight` | Airline service between distinct cities with increasing departure and arrival times |
| `Seat` | Flight-specific unique number, Economy/Business cabin, Window/Middle/Aisle type, and Decimal whole-yen JPY price |
| `Booking` | Unique seat reservation with guest/user data, immutable price amounts, reference, and creation timestamp |

The database prevents two bookings from referencing the same seat. This invariant does
not depend on browser validation or a future seat-map interface.

## Public HTTP Endpoints

All application routes use the `reservations` URL namespace.

| Name | Method and URL | Arguments or fields | Response |
| --- | --- | --- | --- |
| `reservations:home` | `GET /` | None | Renders the home page and flight-search entry; status 200 |
| `reservations:flight_list` | `GET /flights/` | Query fields `origin`, `destination`, and `departure_date`; optional `HX-Request: true` header | With no query, renders all flights ordered by ascending departure time. A valid query filters exact cities and departure date in that order. Invalid input renders visible errors and no partially filtered results. Ordinary requests return the complete page; requests with `HX-Request: true` return only the `flight-results` partial; status 200 |
| `reservations:flight_detail` | `GET /flights/<int:flight_id>/` | `flight_id`: database ID of a flight | Renders the airline, route, departure time, and arrival time; status 200, or 404 when the flight does not exist |
| `reservations:flight_booking` | `GET, POST /flights/<int:flight_id>/book/` | URL `flight_id`; POST `seat`, `passenger_name`, `passenger_email`, and `action` | GET shows only the flight's seats. Review displays authoritative prices without persistence. Confirm revalidates and atomically creates a guest booking, then redirects to its receipt. Invalid flights return 404; invalid or stale seats produce visible errors |
| `reservations:booking_confirmation` | `GET /bookings/<str:booking_reference>/confirmation/` | URL `booking_reference` | Displays the immutable booking receipt; unknown references return 404 |
| `reservations:health` | `GET /health/` | None | Returns a non-empty plain-text health response; status 200 |

The flight-search form requires all three fields, resolves origin and destination to
existing cities, rejects a route whose cities are the same, and validates the date
before filtering. It retains `method="get"` and the ordinary `/flights/` action. With
HTMX available, changing any search field or submitting the form sends all three
current values to the same route and replaces only the contents of the stable
`flight-results` region. The node that owns `aria-live` and `aria-atomic` remains in
the document across updates. Without HTMX, the submit button performs the same
complete-page GET as before.

Booking starts from a specific flight result; there is no generic all-flight form.
Only that flight's available seats pass validation. Review and confirmation reject
unknown, cross-flight, or booked identifiers. Final creation runs in a transaction,
while the existing unique-seat constraint remains the final stale/concurrent
double-booking protection. Guest details map to `guest_name` and `guest_email`, and
`Booking.user` remains null.

All amounts are Decimal whole-yen JPY values. A seat's price is the base fare. Taxes
and fees are 10% rounded to the nearest whole yen with `ROUND_HALF_UP`; total is their
sum. The server calculates from the persisted seat and ignores submitted prices.
Confirmed amounts are copied onto `Booking`, so later seat-price changes cannot alter
history. References use a random uppercase `SKY-XXXXXXXX` format and a database unique
constraint.

## Interface and Accessibility

All public HTML pages extend `reservations/base.html` and load
`reservations/static/reservations/styles.css` through Django's static-file system.
The base also loads the pinned HTMX 2.0.4 release from unpkg with integrity metadata
and the `defer` attribute; no custom JavaScript, JavaScript framework, or frontend
build pipeline is used.
The shared page shell provides a skip-to-content link, a stable `main-content` target,
semantic header, named primary navigation, main, and footer landmarks, plus a visible
current-page navigation state.

Page templates use logical headings and semantic sections, articles, forms, and detail
lists. Django continues to render visible labels associated with every form control.
Invalid forms retain submitted values and field-level errors with an announced
summary. Booking seats use native radio controls grouped by cabin and row, explicit
Available/Unavailable text, visible focus, and responsive cards; state never depends
on color alone.

Flight search uses a textual “Updating flight results…” status while enhanced requests
are active. The complete page owns a stable polite, atomic live-region wrapper, and
HTMX replaces only its contents with the reusable result partial. That partial
preserves semantic `ul`/`li` flight cards, keyboard-operable detail links, validation
alerts, and distinct initial and no-match empty states. Complete-page and partial
responses use the same inner result markup.

The stylesheet uses flexible containers, wrapping flex and grid layouts, overflow-safe
sizing, and a narrow-screen media query. Navigation, controls, and buttons become
full-width where appropriate on small screens. Links and controls have visible
`:focus` and `:focus-visible` indicators. No inline CSS or frontend framework is
required.

## Setup

Prerequisites:

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

Install runtime and development dependencies:

```bash
uv sync --all-extras --dev
```

Apply migrations:

```bash
uv run python manage.py migrate
```

Migration `0003` backfills pre-redesign seats with safe classifications and a JPY
15,000 fallback fare, then snapshots existing bookings at that fare with unique
references before enforcing final constraints. It never deletes or disconnects
reservations. Prefer a forward corrective migration after production use; reversing
the schema after new bookings exist requires an export and coordinated application
rollback and must never drop booking data casually.

Populate connected demonstration cities, airlines, future flights, and classified,
varied-price seats:

```bash
uv run python manage.py seed_demo_data
```

The command is safe to repeat. It creates stable seats only when missing and preserves
existing seat records, seeded flight times, bookings, and unrelated data. It never
reschedules a booked flight or rewrites historical booking amounts.

Start the development server:

```bash
uv run python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the home page or
`http://127.0.0.1:8000/admin/` to use Django admin after creating a local superuser:

```bash
uv run python manage.py createsuperuser
```

Local SQLite databases are ignored by Git and must not be committed.

## Production Architecture

Production uses one Render Python Web Service connected to one managed Render
PostgreSQL database:

- GitHub's `main` branch is the deployment source.
- Render uses Python 3.12.8 and installs the frozen `uv.lock` production dependency
  set.
- The free-tier build applies existing Django migrations, initializes demonstration
  data, and then collects static files; WhiteNoise serves compressed, content-hashed
  assets from `STATIC_ROOT`.
- Gunicorn imports `skybook.wsgi:application` and binds to Render's `PORT`.
- Gunicorn's default single worker is adequate for this course/free-tier deployment;
  a scaled production service can set `WEB_CONCURRENCY` later.
- Render terminates HTTPS and forwards the original protocol to Django.
- `/health/` remains the service health-check endpoint.

No uploaded media is currently supported. Render web-service filesystems are
ephemeral, so any future uploaded media must use durable object storage such as an
S3-compatible service. Collected static output is rebuildable and is ignored by Git.

## Deploying to Render

The checked-in [`render.yaml`](render.yaml) is the source of truth for the service
lifecycle. It implements [issues #23](https://github.com/KaswanDevkishan/skybook/issues/23),
[#24](https://github.com/KaswanDevkishan/skybook/issues/24), and
[#25](https://github.com/KaswanDevkishan/skybook/issues/25).

1. Verify the release locally using the commands below.
2. Commit the reviewed files and push the approved revision to GitHub `main`.
3. In the Render dashboard, create a Blueprint and connect this GitHub repository.
4. Review the proposed `skybook` web service and `skybook-postgres` database, then
   apply the Blueprint.
5. Confirm Render generated `SECRET_KEY`, connected `DATABASE_URL`, and set its
   automatic `RENDER` and `RENDER_EXTERNAL_HOSTNAME` variables.
6. Wait for dependency installation, migration, demo-data initialization, static
   collection, and service startup to succeed.
7. Verify `/health/`, a page using `/static/reservations/styles.css`, application
   routes, and Render logs.

Render supplies `RENDER`, `RENDER_EXTERNAL_HOSTNAME`, and `PORT` automatically. The
application variables are:

| Variable | Required | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | On Render | A generated secret used for Django signing; never commit it |
| `DATABASE_URL` | For PostgreSQL | Render's internal database connection string, wired by the Blueprint |
| `DEBUG` | No | Strict boolean; defaults to `false` and must remain `false` on Render |
| `SECURE_HSTS_SECONDS` | No | HSTS duration; defaults to a cautious 3600 seconds on Render |
| `ALLOWED_HOSTS` | Conditional | Comma-separated exact hostnames; required when Render does not supply `RENDER_EXTERNAL_HOSTNAME`, with localhost defaults only outside Render |
| `CSRF_TRUSTED_ORIGINS` | Conditional | Comma-separated origins including schemes; defaults to the Render HTTPS origin, but must be explicit when that hostname is unavailable |
| `DJANGO_DB_PATH` | Local only | Optional path overriding the local SQLite file |

Accepted boolean values are `true`, `false`, `1`, `0`, `yes`, `no`, `on`, and `off`
(case-insensitive). Invalid values fail configuration. Render also rejects
`DEBUG=true`, a missing `SECRET_KEY`, and missing or empty Render host/origin
configuration.

The Blueprint uses these exact lifecycle commands:

```bash
# Build
uv sync --frozen --no-dev && uv run python manage.py migrate && uv run python manage.py seed_demo_data && uv run python manage.py collectstatic --noinput

# Start
uv run gunicorn skybook.wsgi:application --bind 0.0.0.0:$PORT
```

The `&&` chaining stops the build immediately if dependency installation, migration,
demo-data initialization, or static collection fails. Migrations run during the build
because Render pre-deploy commands and Shell access are unavailable to free web
services. If the service is upgraded to a paid plan, preferably move migration back to
a `preDeployCommand` so it runs as a distinct release step.

Render automatically runs `seed_demo_data` after migrations on every deployment. This
ensures the course demonstration has cities, airlines, future searchable flights, and
available seats even when PostgreSQL starts empty. The command is deliberately
idempotent: it creates each seeded flight's schedule only once, preserves that schedule
on later deployments, and never reschedules existing bookings. It also preserves
unrelated records. This is appropriate for SkyBook's course demonstration; a real
production reservation system would normally initialize and maintain operational data
through authenticated admin tools or reviewed, controlled import processes instead of
automatic demo seeding.

The Blueprint injects Render PostgreSQL's internal `DATABASE_URL`; `ssl_require` is
not necessary for that internal connection. Never commit either the internal or
external connection URL.

Free Render PostgreSQL databases expire 30 days after creation and are later deleted
unless upgraded. Treat the course database as temporary and preserve any required data
before expiry.

Do not use `runserver` in production. Free web services have no Render Shell, so
manual production management commands require another safe execution path. To create
a superuser on the free plan, temporarily set `DATABASE_URL` in a local terminal to
the database's Render external connection URL and run the interactive command:

```bash
read -r -s "SKYBOOK_RENDER_DATABASE_URL?Render external DATABASE_URL: "
DATABASE_URL="$SKYBOOK_RENDER_DATABASE_URL" uv run python manage.py createsuperuser
unset SKYBOOK_RENDER_DATABASE_URL
```

The silent prompt keeps the URL out of the command history; clear the variable even if
the command is interrupted. Never save the URL in the repository, `.env`, command
scripts, screenshots, or logs. A paid service can instead use Render Shell or an
authorized one-off job.

## Verification

Run Django system and migration checks:

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

Format and lint:

```bash
uv run ruff format .
uv run ruff format --check .
uv run ruff check .
```

Run tests with the configured coverage report:

```bash
uv run pytest
```

Verify production configuration with non-secret example values. This example uses
SQLite so it does not contact a database; Render uses the injected PostgreSQL
`DATABASE_URL`:

```bash
RENDER=true \
SECRET_KEY=deployment-check-only-not-a-real-secret \
RENDER_EXTERNAL_HOSTNAME=skybook.onrender.com \
uv run python manage.py check --deploy
```

The deployment check intentionally retains Django's HSTS subdomain and preload
advisories. `SECURE_HSTS_SECONDS` is enabled, but
`SECURE_HSTS_INCLUDE_SUBDOMAINS` and `SECURE_HSTS_PRELOAD` remain false because a
SkyBook service does not control Render's parent `onrender.com` domain and should not
make an irreversible preload commitment merely to silence advisory checks.

Verify static collection and the WSGI import:

```bash
uv run python manage.py collectstatic --noinput
uv run gunicorn skybook.wsgi:application --check-config
```

Validate the active booking-redesign OpenSpec change:

```bash
openspec validate redesign-connected-booking-flow --strict
```

CI runs dependency installation, Ruff formatting and lint checks, and Pytest.

## Production Troubleshooting and Rollback

- **Configuration startup failure:** inspect Render logs for the named missing or
  malformed variable. Generate `SECRET_KEY` in Render, use `DEBUG=false`, and enter
  hostnames without schemes in `ALLOWED_HOSTS`; trusted CSRF origins require
  `https://`.
- **Database connection or migration failure:** confirm `DATABASE_URL` is wired from
  `skybook-postgres`, inspect the build log, and redeploy only after identifying the
  failed operation. Free services cannot inspect it through Render Shell. Never
  replace production PostgreSQL with an app-local SQLite file.
- **Missing static assets:** inspect build logs for `collectstatic`, confirm WhiteNoise
  follows `SecurityMiddleware`, and redeploy after fixing any missing manifest entry.
- **Redirect loop or CSRF failure:** preserve Render's forwarded-protocol handling and
  verify the public HTTPS origin appears in `CSRF_TRUSTED_ORIGINS`.
- **Unhealthy service:** check `/health/`, Gunicorn startup logs, the supplied `PORT`,
  and Render service events before changing application behavior.

For a code rollback, redeploy the previous known-good Render deploy or revert the
offending commit and let CI-gated deployment rebuild it. The selected revision's build
will run migrations again, so review its migration state before redeploying. Keep
PostgreSQL intact.
Database rollback is a separate, higher-risk operation: prefer a forward corrective
migration in a new revision. Reverse a migration only through an authorized paid
Shell/one-off job or a carefully secured local connection after confirming it is
reversible and reviewing its data impact. Free-plan backup and retention limitations
mean an earlier database state may not be recoverable.

## OpenSpec and Review

Meaningful changes follow the specifications under `openspec/`. The Exercise 5 Django
foundation and schema are defined by the archived `create-initial-django-schema`
change, and the basic HTTP views by `add-basic-django-views`. Exercise 8 form handling
is defined by `implement-django-forms` and relates to
[issue #11](https://github.com/KaswanDevkishan/skybook/issues/11),
[issue #12](https://github.com/KaswanDevkishan/skybook/issues/12), and
[issue #13](https://github.com/KaswanDevkishan/skybook/issues/13).
Exercise 9 interface work is defined by `improve-exercise-9-interface` and relates to
[issue #15](https://github.com/KaswanDevkishan/skybook/issues/15) (responsive SkyBook
styling), [issue #16](https://github.com/KaswanDevkishan/skybook/issues/16) (responsive
layout), and [issue #17](https://github.com/KaswanDevkishan/skybook/issues/17)
(interface accessibility).
Exercise 10's server-driven flight search is defined by `add-htmx-flight-search` and
relates to [issue #19](https://github.com/KaswanDevkishan/skybook/issues/19),
[issue #20](https://github.com/KaswanDevkishan/skybook/issues/20), and
[issue #21](https://github.com/KaswanDevkishan/skybook/issues/21).
Exercise 11's Render deployment is defined by `deploy-skybook-to-render` and relates
to [issue #23](https://github.com/KaswanDevkishan/skybook/issues/23),
[issue #24](https://github.com/KaswanDevkishan/skybook/issues/24), and
[issue #25](https://github.com/KaswanDevkishan/skybook/issues/25).

AI-assisted changes require human review before commit. Inspect the final state with:

```bash
git status
git diff
```

Do not commit `SECRET_KEY`, `DATABASE_URL`, tokens, passwords, Render credentials, API
keys, `.env` files, virtual environments, caches, coverage output, collected static
output, or local database files. Production secrets must be supplied through the
environment; the checked-in fallback secret is development-only and is rejected as a
Render configuration substitute.
