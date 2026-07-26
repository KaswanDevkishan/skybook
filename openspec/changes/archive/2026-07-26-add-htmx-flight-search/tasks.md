## 1. Response and Template Tests

- [x] 1.1 Add tests proving ordinary GET requests use the complete flight-list page
  while `HX-Request: true` GET requests use only the reusable result partial and omit
  the page shell and search form.
- [x] 1.2 Add HTMX response tests for exact filtered and ordered matches, invalid-form
  validation feedback with no partial filtering, and valid empty-result feedback.
- [x] 1.3 Add template tests for the pinned HTMX script and the form's exact `hx-get`,
  change-and-submit `hx-trigger`, `hx-target`, `hx-swap`, and `hx-indicator` contract.
- [x] 1.4 Extend accessibility and semantic tests for visible labels, skip navigation,
  semantic `ul`/`li` cards, textual loading status, live-result semantics, validation
  alerts, keyboard-usable links, and retained progressive-enhancement markup.

## 2. Server-Driven Flight Search

- [x] 2.1 Add the pinned HTMX script to the shared base template without a JavaScript
  framework or custom JavaScript.
- [x] 2.2 Create
  `reservations/templates/reservations/partials/flight_results.html` with the result
  contents, validation summary, semantic flight cards, and empty state.
- [x] 2.3 Refactor the complete flight-list template to include the partial once and
  enhance its existing GET form with complete-form change and submit requests,
  `innerHTML` targeting of a stable live-region owner, and an associated textual
  loading indicator.
- [x] 2.4 Update namespaced CSS to preserve responsive flight-card presentation and
  provide visible, non-animation-only HTMX loading feedback.
- [x] 2.5 Update `flight_list` to select the partial only when the `HX-Request` header
  equals `true`, while sharing the existing form binding, validation, queryset
  filtering, ordering, and context with ordinary requests.

## 3. Scope and Contributor Documentation

- [x] 3.1 Update `README.md` with the Exercise 10 interaction, pinned dependency,
  ordinary and HTMX response contracts, progressive enhancement and accessibility
  behavior, non-goals, and GitHub issues #19, #20, and #21.
- [x] 3.2 Update `AGENTS.md` from Exercise 9 to Exercise 10 where needed, permitting only
  the focused HTMX result update while preserving model, migration, validation,
  booking, duplicate-seat, framework, and deferred-feature boundaries.
- [x] 3.3 Confirm no model or migration file changed and that the OpenSpec change remains
  coherent with the implemented templates, view, tests, and documentation.

## 4. Verification

- [x] 4.1 Run `uv run ruff format .` and review the formatting changes.
- [x] 4.2 Run `uv run ruff check .`.
- [x] 4.3 Run `uv run pytest` and confirm existing and new coverage remains passing.
- [x] 4.4 Run `uv run python manage.py check`.
- [x] 4.5 Run `uv run python manage.py makemigrations --check --dry-run` and confirm
  Django reports no model changes.
- [x] 4.6 Run `openspec validate add-htmx-flight-search --strict` and resolve any artifact
  validation errors.
