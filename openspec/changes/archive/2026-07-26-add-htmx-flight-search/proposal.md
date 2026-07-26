## Why

Exercise 10 needs one focused server-driven interaction that makes flight search feel
immediate without replacing Django's validated GET workflow or weakening progressive
enhancement. Updating only the matching-flight region with HTMX demonstrates that
interaction while preserving the complete page for ordinary requests.

## What Changes

- Load a pinned HTMX release from the shared base template without adding a client-side
  framework or custom JavaScript.
- Enhance the existing GET flight-search form so field changes and form submission send
  all current values to the existing flight-list route and replace only the results
  region.
- Add an accessible textual loading indicator and live/status semantics that preserve
  keyboard and screen-reader usability.
- Extract flight results, empty states, and search-validation feedback into one reusable
  partial used by both complete-page and HTMX responses.
- Detect the `HX-Request` header in the existing Django view while reusing
  `FlightSearchForm`, filtering, ordering, and ordinary full-page behavior.
- Add request, filtering, validation, empty-state, markup, accessibility, documentation,
  and migration-safety tests.
- Update contributor and OpenSpec documentation for the Exercise 10 contract and related
  GitHub issues #19, #20, and #21.
- Keep models and migrations unchanged. Dynamic seat maps, checkout, authentication UI,
  payments, external airline APIs, and other client-side frameworks remain non-goals.

This work is within Exercise 10's allowed scope because it adds one progressively
enhanced, server-rendered interaction to the existing Django flight search.

## Capabilities

### New Capabilities

- `server-driven-flight-search`: Defines HTMX request markup, header-based partial
  responses, reusable flight-result rendering, loading feedback, and progressive
  enhancement.

### Modified Capabilities

- `basic-reservation-views`: Extends the flight-list response contract to return either
  the complete page or the result partial according to the `HX-Request` header.
- `accessible-responsive-interface`: Adds accessible asynchronous loading and
  result-update semantics to the existing interface requirements.
- `repository-agent-guidance`: Updates the documented exercise scope and verification
  expectations for the HTMX interaction.

## Impact

The change affects the shared base template, flight-list template, a new reservations
partial template, the flight-list view, namespaced CSS, view/template tests, `README.md`,
`AGENTS.md`, and OpenSpec requirements. It adds a pinned browser dependency on HTMX but
does not alter routes, forms, database models, migrations, persistence, or booking
behavior.
