## MODIFIED Requirements

### Requirement: Root redirects to flight search
The root route SHALL accept GET requests at `/` and return a normal non-permanent Django
redirect to `/flights/`. The application SHALL NOT render or retain a separate landing
page template. The SkyBook brand SHALL link directly to `/flights/`.
The shared primary navigation SHALL omit a separate Home item and SHALL contain Flights,
My Bookings, and real authentication-state-appropriate account actions. Logged-out users
SHALL see Sign In and Create Account; logged-in users SHALL see Account and a
CSRF-protected POST Log Out action. It MUST NOT contain fake or disabled authentication
links.

#### Scenario: Visitor opens the root route
- **WHEN** an anonymous visitor sends GET `/`
- **THEN** the response redirects to `/flights/`, whose shared header brand links to
  `/flights/` and whose logged-out navigation has no separate Home item

#### Scenario: Authenticated user follows the root redirect
- **WHEN** an authenticated user sends GET `/`
- **THEN** the response redirects to `/flights/`, where navigation contains Flights,
  My Bookings, Account, and a POST Log Out action and omits Sign In and Create Account

#### Scenario: Visitor views flight search after homepage removal
- **WHEN** a visitor opens `/flights/`
- **THEN** the old landing-page eyebrow, heading, and description are not rendered

### Requirement: Flight-search hero copy
The complete flight-search page SHALL present only the heading “Take off toward your next
adventure” above the search form. It SHALL NOT present the eyebrow “YOUR JOURNEY STARTS
HERE” or the description “Discover routes across Japan, compare fares, and choose the seat
that suits your journey.” The search form SHALL follow the heading without an empty gap
reserved for the removed copy. The page SHALL preserve the existing navy hero design,
semantic heading association, responsive layout, and accessibility.

#### Scenario: Visitor opens the flight-search page
- **WHEN** a visitor sends an ordinary GET request to `/flights/`
- **THEN** the complete response renders only the supplied heading above the search form,
  omits the eyebrow and description, and leaves no empty copy spacing between them

## ADDED Requirements

### Requirement: Named authentication and account URL surface
The application SHALL expose named routes for registration, sign in, POST sign out,
account dashboard, and guest My Bookings information alongside the preserved reservation
routes. Account and user-owned booking destinations SHALL enforce their authentication
and ownership contracts.

#### Scenario: Caller reverses account routes
- **WHEN** a caller reverses each authentication, account, or guest My Bookings route
- **THEN** Django returns the documented local path for that named route

#### Scenario: Caller uses unsupported logout method
- **WHEN** a caller sends a method other than POST to the logout route
- **THEN** the response rejects the method without changing authentication state

### Requirement: Named cancellation URL supports display and protected transition
The application SHALL expose an owner-scoped booking cancellation route. GET SHALL only
render confirmation, POST SHALL be CSRF protected, and successful cancellation SHALL
redirect to My Bookings.

#### Scenario: Owner opens and submits cancellation
- **WHEN** the owner sends GET and then a valid POST for a future confirmed booking
- **THEN** GET leaves status unchanged and POST cancels then redirects to My Bookings

### Requirement: Existing connected search and booking journey remains compatible
The new account routes and navigation SHALL preserve ordinary and HTMX flight search,
flight-scoped seat selection, editable passenger entry, authoritative review, atomic
confirmation, historical guest receipts, JPY pricing, cancellation, and duplicate-seat
behavior. Authentication MUST be required before price review and final confirmation.

#### Scenario: Anonymous visitor reaches seat selection
- **WHEN** an anonymous visitor selects a seat and enters valid passenger data
- **THEN** the page offers authentication actions instead of price review and creates no
  Booking

#### Scenario: Signed-in visitor completes booking
- **WHEN** an authenticated visitor completes the same connected journey
- **THEN** the journey completes with an owned booking and unchanged price and seat safety

### Requirement: Invalid past-date searches return no flight results
Ordinary and strict HTMX flight searches with a departure date before Django's current
local date SHALL render the departure-date field error and MUST NOT query or display
flight results. Both response modes SHALL use the same validation message while
preserving the existing complete-page and partial-template boundaries.

#### Scenario: Complete-page past-date search
- **WHEN** a visitor submits a past departure date without an HTMX request header
- **THEN** the complete page associates “Departure date cannot be in the past.” with the
  date input and displays no flight results

#### Scenario: HTMX past-date search
- **WHEN** a visitor submits the same past departure date with `HX-Request: true`
- **THEN** the results partial contains the same associated validation message and no
  flight results

### Requirement: Booking review and confirmation require authentication
An anonymous POST toward price review SHALL preserve only safe validated pending-booking
fields and redirect to authentication through a safe local destination. Final
confirmation SHALL require authentication, and every newly completed public booking
MUST belong to `request.user`.

#### Scenario: Anonymous caller posts directly to review
- **WHEN** an anonymous caller submits valid flight, seat, passenger name, and passenger
  email data to the review path
- **THEN** no Booking is created and the response redirects to authentication

#### Scenario: Anonymous caller posts directly to confirmation
- **WHEN** an anonymous caller submits a confirmation request
- **THEN** no Booking is created and the response redirects to authentication
