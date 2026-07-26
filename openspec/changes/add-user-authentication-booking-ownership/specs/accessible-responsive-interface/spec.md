## ADDED Requirements

### Requirement: Authentication pages are accessible and responsive
Registration and sign-in pages SHALL use semantic CSRF-protected forms, visible labels,
accessible validation feedback, consistent form controls and actions, and responsive
premium navy cards. Password controls MUST NOT render submitted password values after an
invalid submission.

#### Scenario: Visitor uses an authentication card on mobile
- **WHEN** a registration or sign-in page is displayed at a narrow viewport
- **THEN** its headings, labels, controls, errors, and actions remain readable, operable,
  and contained within the viewport

#### Scenario: Keyboard user corrects authentication errors
- **WHEN** a keyboard user traverses an invalid authentication form
- **THEN** errors are announced or associated with controls and every interactive element
  has a visible focus state

#### Scenario: Failed sign-in alert remains readable
- **WHEN** failed credentials render in the sign-in card at mobile or desktop width
- **THEN** one compact high-contrast alert remains inside the card with consistent
  padding, border, radius, and line height and no clipped, overlapping, or overflowing
  text

### Requirement: Account booking history is readable and responsive
The account dashboard SHALL present profile data and owned booking history in semantic,
readable cards or equivalent grouped content. Each booking SHALL have programmatically
understandable labels for its reference, route, departure, seat, price, and status when
present, and the layout SHALL adapt without horizontal page overflow.

#### Scenario: User reviews booking history on a narrow screen
- **WHEN** an authenticated user opens an account containing multiple bookings at mobile
  width
- **THEN** every booking remains visually grouped, labeled, readable, and within the
  viewport

#### Scenario: Booking history reflects cancellation eligibility
- **WHEN** the account contains future confirmed, cancelled, and past bookings
- **THEN** only the future confirmed booking has a Cancel booking action, the cancelled
  booking has a clear Cancelled badge, and past bookings have no cancellation action

### Requirement: Cancellation feedback is accessible
The cancellation confirmation SHALL use semantic headings and details, a clear warning,
a CSRF-protected form, and accessible success or rejection messages.

#### Scenario: Owner reviews cancellation
- **WHEN** the owner opens a cancellation confirmation
- **THEN** the warning, booking details, simulated-payment/no-refund notice, and protected
  action are readable and keyboard operable

### Requirement: Authentication-aware navigation remains operable
Authentication-aware navigation SHALL remain keyboard accessible and usable at desktop
and mobile widths. Its POST Log Out button SHALL receive the same visible focus and
readable interaction treatment as navigation links, and current destinations SHALL expose
`aria-current="page"` where practical.

#### Scenario: Keyboard user operates member navigation
- **WHEN** an authenticated keyboard user traverses the primary navigation
- **THEN** Flights, My Bookings, Account, and Log Out are reachable with visible focus and
  Log Out submits through its protected form

### Requirement: Seat-selection actions communicate authentication gating
The logged-out seat-selection page SHALL display the notice “Sign in or create an account
to continue your booking.”, a primary “Sign in to continue” button, and a secondary
“New to SkyBook? Create an account” link while retaining editable seat and passenger
controls. The logged-in page SHALL display “Review price” as its primary action.

#### Scenario: Anonymous visitor reviews seat-selection actions
- **WHEN** the seat-selection page renders for an anonymous visitor
- **THEN** authentication notice and actions are present and Review price is absent

#### Scenario: Authenticated visitor reviews seat-selection actions
- **WHEN** the seat-selection page renders for an authenticated user
- **THEN** Review price is the primary action and passenger details remain editable
