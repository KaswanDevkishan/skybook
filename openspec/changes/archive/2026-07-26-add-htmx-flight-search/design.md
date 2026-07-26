## Context

SkyBook already has a Django `FlightSearchForm`, a GET-only `/flights/` view, ordered
queryset filtering, semantic result cards, accessible validation, and responsive
namespaced CSS. Exercise 10 adds one server-driven interaction across the shared
template, search page, result rendering, view response selection, tests, and
documentation. The interaction must remain useful when HTMX is unavailable and must
not change models, migrations, routes, or booking behavior.

## Goals / Non-Goals

**Goals:**

- Make changes to origin, destination, or departure date refresh matching flights
  without a whole-page navigation.
- Keep explicit form submission and ordinary browser GET navigation working.
- Share one result template between full-page and HTMX responses.
- Preserve Django form validation and filtering as the single source of truth.
- Announce loading, validation, empty, and updated-result states accessibly.
- Pin the small browser dependency and verify the response boundary with tests.

**Non-Goals:**

- Dynamic seat maps, checkout, authentication UI, payments, external airline APIs, or
  the complete booking workflow.
- New models, schema fields, migrations, endpoints, JavaScript frameworks, or a
  client-side filtering implementation.
- Custom JavaScript for focus management or request orchestration.

## Decisions

### Enhance the existing GET form declaratively

The flight-search `<form>` will retain `method="get"` and its existing named route in
`action`, and will add `hx-get` for that same URL. A form-level `hx-trigger` will cover
the relevant control changes and normal submit event, so every HTMX request serializes
the complete form rather than only the control that changed. `hx-indicator` will point
to a persistent textual status element.

Putting the attributes on individual controls was rejected because it would duplicate
configuration and makes complete-form serialization less obvious. Custom JavaScript
listeners were rejected because HTMX attributes cover the interaction.

### Replace one self-contained result region

The reusable partial will own a section with the stable `flight-results` ID. The form
will target `#flight-results` and use `outerHTML`, allowing every response to replace
the complete region while retaining the same stable ID for later requests. The partial
will include the results heading, validation summary when applicable, semantic
`ul`/`li` flight cards, and the empty state.

Replacing `innerHTML` was considered, but `outerHTML` keeps the partial self-contained
and prevents the full-page template from duplicating the result-region wrapper.
Replacing the entire page or form was rejected because Exercise 10 calls for a focused
result update and stable controls.

### Branch only at template selection

The view will always instantiate the same `FlightSearchForm`, build the same ordered
queryset, validate the same query values, and create the same context. It will inspect
`request.headers.get("HX-Request") == "true"` to select either the partial or
`reservations/flight_list.html`.

This direct header check avoids an additional Django integration package for a single
interaction. Splitting out a second endpoint was rejected because the existing route
already owns the search contract and the requested response varies only by
representation.

### Keep progressive enhancement and accessibility in server-rendered markup

The submit button remains present, labels and Django field markup remain unchanged,
and the form `action` continues to support a full-page GET without HTMX. The indicator
will contain explicit loading text, use status/live semantics, and be associated through
`hx-indicator`; CSS may control its request-time visibility but animation will not be
the only signal. The result section will be a polite live region with an atomic update
boundary so server-rendered validation, empty, and result messages are announced.

Validation feedback returned in an HTMX response will live inside the targeted result
partial, while the ordinary full page continues to render the same feedback from that
partial and retains Django's labeled fields and submitted control values.

### Pin HTMX in the shared base

The base template will load a specific HTMX 2.x patch version from a CDN. The exact
version, URL, and integrity metadata will be asserted in tests and documented so an
upstream release cannot silently change runtime behavior. Vendoring was considered,
but a pinned script is sufficient for this course-sized interaction and avoids adding
a frontend build pipeline.

## Risks / Trade-offs

- [Automatic changes can issue several GETs while selecting search criteria] → Scope
  triggers to the three controls and use a short declarative delay where useful; every
  intermediate response remains safe and idempotent.
- [A CDN outage disables HTMX] → The form remains a standard GET form and the submit
  button provides full-page navigation.
- [Screen readers differ in live-region announcement behavior] → Use visible status
  text plus conservative `role="status"`/`aria-live="polite"` semantics and retain
  ordinary page behavior.
- [A forged or differently cased header could select the wrong representation] → Treat
  only the explicit normalized Django header value `"true"` as an HTMX request and test
  positive and ordinary cases.
- [The partial can drift from full-page result markup] → Make the full page include the
  partial and test that result markup appears exactly once.

## Migration Plan

No database migration is required. Add the template and view response branch, then
update tests, CSS, README, agent guidance, and OpenSpec documents. Verify tests, Django
checks, migration drift, formatting, and linting. Rollback consists of removing the
HTMX script and attributes, restoring full-page-only template selection, and inlining
the partial if desired; stored data is unaffected.

## Open Questions

None. The existing route, validated fields, target region, response header, and
excluded features are specified.
