## ADDED Requirements

### Requirement: Shared semantic page structure
Every rendered reservation page SHALL provide a skip-to-content link whose target is a
stable main-content ID, a header, an understandably named primary navigation landmark,
one main landmark, and a footer. Page content SHALL use semantic sections, articles,
forms, and headings where appropriate, maintain a logical heading hierarchy, and avoid
presentation-only wrappers.

#### Scenario: Visitor navigates page landmarks
- **WHEN** a visitor opens any reservation HTML page
- **THEN** the response contains the shared landmarks and a skip link targeting the
  stable main-content element

#### Scenario: Visitor reads page structure
- **WHEN** a visitor or assistive technology traverses a reservation page
- **THEN** headings and page-specific semantic elements describe the content in a
  logical order

### Requirement: External consistent presentation
The application SHALL load `reservations/styles.css` from Django's static-file system
in the shared base template and SHALL NOT use inline CSS. The stylesheet SHALL provide
consistent typography, spacing, colors, borders, buttons, navigation, forms, validation
feedback, flight results, and empty-state presentation.

#### Scenario: Visitor opens a styled page
- **WHEN** a visitor opens a reservation HTML page
- **THEN** the document links the namespaced external stylesheet and inherits the
  shared visual system

### Requirement: Responsive layout
The interface SHALL use flexible containers and grid or flex layouts that support
desktop, tablet, and mobile widths without horizontal page overflow. Form controls and
buttons SHALL remain usable on small screens, and the stylesheet SHALL include a
simple narrow-screen media query without relying on a JavaScript framework.

#### Scenario: Visitor uses a narrow viewport
- **WHEN** a reservation page is displayed at a mobile width
- **THEN** navigation, content, forms, controls, and actions adapt within the viewport
  without requiring horizontal page scrolling

### Requirement: Visible keyboard interaction
Interactive elements SHALL have clearly visible `:focus` and `:focus-visible` styles,
and foreground/background combinations SHALL provide readable contrast. Primary
navigation SHALL expose `aria-current="page"` for the current destination where
practical.

#### Scenario: Keyboard user traverses controls
- **WHEN** a keyboard user focuses links, controls, or buttons
- **THEN** the focused element has a visible focus indicator

#### Scenario: Assistive technology reads primary navigation
- **WHEN** a visitor opens a primary navigation destination
- **THEN** the navigation has an accessible name and identifies the current page where
  practical

### Requirement: Accessible validation presentation
Validation feedback SHALL remain visible, SHALL NOT rely on color alone, and SHALL use
`role="alert"` or equivalent semantics for validation summaries where appropriate.
Django-rendered labels and error associations SHALL be preserved for every form
control.

#### Scenario: Invalid form is rendered
- **WHEN** search or booking input fails validation
- **THEN** the page presents an announced validation summary plus visible field-level
  feedback associated with labeled controls
