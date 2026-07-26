## Context

SkyBook currently renders five small Django templates from a shared base. The pages
already provide working GET search and POST booking forms, but the base has no static
stylesheet, the main landmark has no skip target, navigation has no accessible name or
current-page state, validation is visually unstructured, and lists/forms have no
responsive presentation. The change crosses shared and page-specific templates,
static assets, tests, and documentation, while the existing views, forms, routes, and
database protections remain authoritative.

## Goals / Non-Goals

**Goals:**

- Establish a small semantic page shell shared by every public HTML page.
- Provide a cohesive external CSS system that works across desktop, tablet, and
  narrow mobile screens.
- Make navigation, focus, validation, form labels, flight results, and empty states
  understandable and usable with keyboards and assistive technology.
- Test stable interface contracts without coupling tests to incidental copy or every
  CSS declaration.
- Preserve all Exercise 8 request handling, validation, persistence, and database
  behavior.

**Non-Goals:**

- Changing Python view/form logic, URLs, models, migrations, or booking invariants.
- Adding authentication screens, payments, seat maps, external APIs, a complete
  booking flow, a frontend framework, JavaScript behavior, or production branding.
- Claiming formal WCAG conformance or introducing automated browser/audit tooling.

## Decisions

### Use one namespaced static stylesheet

`base.html` will load `reservations/styles.css` through `{% load static %}` and
`{% static %}`. A single namespaced asset fits this small application, avoids inline
styles and new build dependencies, and gives every extending template the same design
tokens and responsive rules. Per-page stylesheets and CSS frameworks were rejected as
unnecessary fragmentation and dependency overhead.

### Make the base template own global accessibility landmarks

The shared base will own the skip link, `header`, named primary `nav`, stable
`main-content` target, messages, and `footer`. Page templates will use `section`,
`article`, navigation, lists, definitions, and forms only where those elements
describe their content. This avoids repeating global semantics and avoids adding
wrapper elements solely for styling.

Each page will supply a page identifier through a template block so the corresponding
primary-navigation link can render `aria-current="page"`. This keeps the current-page
state server-rendered and avoids view-context or JavaScript changes. A named navigation
landmark makes its purpose clear to screen-reader users.

### Keep Django's controls and label/error machinery

Forms will continue to render each bound field's `label_tag`, widget, help/error
metadata, and submitted value. Templates will group fields semantically and expose
validation summaries with `role="alert"` while retaining field-level errors adjacent
to their controls. Error styling will combine text/icon-like markers, borders, and
color so color is not the only signal. Replacing forms with hand-authored inputs was
rejected because it risks breaking IDs, labels, values, validation, and CSRF behavior.

### Use resilient CSS layout and focus treatment

The stylesheet will use a constrained flexible container, fluid sizing, wrapping
flex/grid layouts, `box-sizing: border-box`, and overflow-safe text/content rules.
Controls and buttons will meet the container width on narrow screens, and one simple
media query will stack navigation/actions and reduce spacing. `:focus` provides a
visible fallback and `:focus-visible` refines keyboard focus without removing it.
Colors will be selected for readable contrast in normal, interactive, focus, and
error states.

### Test contracts at the rendered-HTML boundary

Django client tests will assert the static stylesheet URL, skip-link/target pair,
landmarks, accessible navigation, representative page structure, visible labels, and
alert semantics on invalid search and booking submissions. Existing behavioral tests
remain in place to prove search filtering, retained values, CSRF, persistence,
redirects, and duplicate rejection are unchanged. Tests will avoid asserting complete
markup snapshots or pixel layout, which would be brittle without increasing contract
confidence.

## Risks / Trade-offs

- [Template tests can become coupled to cosmetic markup] → Assert stable semantic
  contracts and URLs, not complete HTML strings or class ordering.
- [Django's default error rendering may duplicate messages between summary and fields]
  → Keep a concise alert container and field errors where they preserve control
  association; verify the rendered output with invalid submissions.
- [A single mobile breakpoint cannot optimize every device] → Prefer intrinsically
  flexible layouts first and use the breakpoint only for narrow-screen adjustments.
- [Server-rendered `aria-current` blocks add small template repetition] → Keep the
  state logic in the shared navigation and verify each practical destination.

## Migration Plan

1. Add the namespaced static asset and load it from the shared base.
2. Refine shared and page-specific semantics without changing form actions or field
   rendering.
3. Add focused template/accessibility tests and run the existing behavioral suite.
4. Update README, repository guidance, and interface documentation with references to
   #15 Add responsive SkyBook styling, #16 Improve responsive layout, and #17 Improve
   interface accessibility.
5. Run formatting, lint, Django checks, migration drift checks, and the full tests.

Rollback consists of reverting the template, stylesheet, test, and documentation
changes. No data migration, dependency rollback, or persistent-state repair is needed.

## Open Questions

None. The related Exercise 9 work is tracked by #15 Add responsive SkyBook styling,
#16 Improve responsive layout, and #17 Improve interface accessibility.
