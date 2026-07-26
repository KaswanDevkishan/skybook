## 1. Interface Contract Tests

- [x] 1.1 Add rendered-page tests for the external stylesheet URL, skip-link and
  `main-content` target, global landmarks, named primary navigation, and practical
  `aria-current="page"` states.
- [x] 1.2 Add page-specific tests for logical headings and important semantic
  `section`, `article`, `form`, list, detail, and empty-state elements.
- [x] 1.3 Add search and booking form tests that verify visible labels remain
  associated with control IDs and invalid submissions render alert semantics while
  retaining Django field errors and values.

## 2. Shared Semantic Shell

- [x] 2.1 Update `base.html` to load Django static assets, link the external
  stylesheet, and provide the skip link, stable main target, semantic header, named
  primary navigation, current-page state, accessible messages, and footer.
- [x] 2.2 Update `home.html` with a logical page heading and concise semantic welcome
  and action regions without changing link destinations.
- [x] 2.3 Update `flight_list.html` with semantic search, results, flight-item, and
  empty-state markup without changing GET fields, form action, result iteration, or
  detail links.
- [x] 2.4 Update `flight_detail.html` with an appropriately labeled semantic flight
  region while preserving all displayed flight values.
- [x] 2.5 Update `booking_form.html` with semantic form structure and accessible
  validation feedback without changing POST action, CSRF, fields, or submit behavior.

## 3. Responsive External Styling

- [x] 3.1 Create `reservations/static/reservations/styles.css` with shared design
  tokens and consistent typography, spacing, containers, colors, contrast, borders,
  navigation, buttons, forms, errors, flight results, and empty states.
- [x] 3.2 Add visible `:focus` and `:focus-visible` treatment plus non-color validation
  indicators for links, fields, and actions.
- [x] 3.3 Add intrinsic overflow-safe flex/grid behavior and a simple narrow-screen
  media query that stacks navigation, forms, controls, and buttons where needed.
- [x] 3.4 Inspect rendered desktop, tablet, and mobile layouts to confirm content does
  not overflow horizontally and keyboard focus and form controls remain usable.

## 4. Documentation and Scope

- [x] 4.1 Reference the verified related issues—#15 Add responsive SkyBook styling,
  #16 Improve responsive layout, and #17 Improve interface accessibility—in the
  Exercise 9 documentation.
- [x] 4.2 Update `README.md` with the Exercise 9 semantic, static CSS, responsive, and
  accessibility interface contract plus the verified related issue references.
- [x] 4.3 Update `AGENTS.md` from Exercise 8 to the Exercise 9 scope where necessary,
  retaining all existing Django, domain, security, testing, and deferred-feature
  constraints.
- [x] 4.4 Review the implemented interface against this change's OpenSpec documents
  and reconcile documentation if implementation details require clarification.

## 5. Verification

- [x] 5.1 Run `uv run ruff format .` and `uv run ruff check .`.
- [x] 5.2 Run `uv run pytest` and confirm existing search, booking, CSRF, retained-value,
  duplicate-seat, and view behavior still passes alongside the new interface tests.
- [x] 5.3 Run `uv run python manage.py check` and
  `uv run python manage.py makemigrations --check --dry-run` to verify system health
  and that no schema changes were introduced.
- [x] 5.4 Run
  `openspec validate improve-exercise-9-interface --type change --strict` and resolve
  all artifact or requirement validation errors.
