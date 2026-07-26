## ADDED Requirements

### Requirement: Seat selection is keyboard accessible
Available seat selection SHALL use native keyboard-operable form controls with visible
associated labels and visible focus indicators. Unavailable seats SHALL be disabled
or otherwise non-submittable and MUST include explicit unavailable text; cabin, type,
price, and state MUST NOT be communicated by color alone.

#### Scenario: Keyboard visitor selects a seat
- **WHEN** the visitor tabs through available seat controls and activates one
- **THEN** focus is visible and the selected control can be submitted without a
  pointer device

#### Scenario: Visitor perceives seat state without color
- **WHEN** available and unavailable seats are displayed
- **THEN** text and control semantics distinguish their state in addition to styling

### Requirement: Booking workflow is responsive and semantic
Seat groups, passenger forms, price review, and confirmation details SHALL use
semantic headings, groups, lists or definition structures as appropriate and SHALL
adapt to narrow viewports without horizontal page scrolling or inaccessible controls.

#### Scenario: Visitor uses a mobile viewport
- **WHEN** the seat grid, form, review, or receipt is rendered at a narrow width
- **THEN** content reflows into readable cards or columns with usable controls

#### Scenario: Visitor uses the aircraft map on mobile
- **WHEN** the cabin is wider than the mobile viewport
- **THEN** the seat-map region scrolls horizontally, the whole page does not, seat
  targets remain touch-friendly, and the review action stays available at the bottom

#### Scenario: Visitor uses a desktop or tablet viewport
- **WHEN** the booking page crosses its responsive breakpoints
- **THEN** desktop shows the map beside a sticky details sidebar while tablet stacks
  the sidebar below the map

### Requirement: Workflow errors are accessible
Server validation and availability conflicts SHALL be visibly located near the
relevant control, programmatically associated where applicable, and summarized with
alert semantics. Focus and retained values SHALL support correction without requiring
JavaScript.

#### Scenario: Seat becomes unavailable
- **WHEN** final confirmation loses a double-booking race
- **THEN** the returned page announces a visible availability error and enables the
  visitor to choose another current seat

### Requirement: Booking progressively enhances
The complete booking workflow MUST remain usable with HTML form submissions and full
page responses when JavaScript is disabled. Any vanilla JavaScript behavior SHALL
enhance presentation only, and existing HTMX search fallback SHALL remain intact.

#### Scenario: JavaScript is unavailable
- **WHEN** a visitor searches, selects a seat, reviews a price, and confirms
- **THEN** the journey completes through ordinary links and form submissions

### Requirement: Seat details and selection state are perceivable
Each seat SHALL expose number, cabin, type, formatted JPY fare, and availability on
hover or keyboard focus. Selected and unavailable states SHALL include text or symbols
and native checked/disabled semantics in addition to color. A compact legend SHALL
identify Available, Selected, Unavailable, Business, and Economy.

#### Scenario: Keyboard visitor explores seats
- **WHEN** focus moves to an available seat radio
- **THEN** its associated label has a visible focus indicator and its complete detail
  content is exposed without requiring hover

#### Scenario: Booked seat is displayed
- **WHEN** a seat already has a booking
- **THEN** it remains visible for orientation with an unavailable label, disabled
  control semantics, and a non-color unavailable mark

### Requirement: Flight discovery remains accessible and responsive
The shared header SHALL expose the SkyBook brand as a keyboard-operable homepage link
and Flights as the only primary navigation item, without a separate Home item,
authentication placeholder, or duplicated SkyBook wordmark. Flights SHALL retain
active-page semantics across flight search, detail, and booking routes. Navigation
links SHALL have visible keyboard focus, touch-friendly targets, semantic navigation
markup, and a responsive layout without horizontal page scrolling. The flight-search
hero, form, and result cards SHALL use semantic headings and landmarks, visible
labels, keyboard-visible actions, and mobile-first layouts that do not cause
horizontal page scrolling. Complete-page content SHALL use a readable approximately
1100–1200px maximum width on desktop without scaling or zoom techniques.

#### Scenario: Keyboard visitor uses shared navigation
- **WHEN** a visitor tabs through the shared header
- **THEN** the linked SkyBook brand and Flights item receive visible focus and can be
  activated from the keyboard

#### Scenario: Visitor opens a flight workflow page
- **WHEN** the current route is flight search, flight detail, or flight booking
- **THEN** Flights is marked as the current navigation item

#### Scenario: Navigation is displayed at mobile width
- **WHEN** the shared header is rendered on a narrow viewport
- **THEN** the brand and Flights item remain usable without horizontal page scrolling

#### Scenario: Visitor searches on a narrow viewport
- **WHEN** the flight page is displayed at mobile width
- **THEN** search controls and result cards stack in one column and primary actions
  remain full-width and touch-friendly
