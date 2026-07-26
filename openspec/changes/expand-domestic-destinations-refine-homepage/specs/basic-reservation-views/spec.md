## MODIFIED Requirements

### Requirement: Home page navigation
The `home` view SHALL accept GET requests at `/`, render `reservations/home.html`, and
present the eyebrow “Japan is closer than you think”, heading “Where will Japan take
you next?”, and description “Search domestic routes, compare fares, and choose your
perfect seat—all in one smooth journey.” The SkyBook brand SHALL remain a link to the
homepage. The shared primary navigation SHALL omit a separate Home item and SHALL
contain Flights as its only navigation item. It MUST NOT contain Booking Form, Sign
In, Create Account, or other placeholder navigation. Authentication navigation is
deferred to a separate future change.

#### Scenario: Visitor opens the home page
- **WHEN** a visitor sends GET `/`
- **THEN** the response has status 200, renders the supplied hero copy, the SkyBook
  brand links to `/`, Flights is the only primary navigation item, and no separate
  Home item appears

#### Scenario: Authentication is not implemented
- **WHEN** a visitor inspects the shared primary navigation
- **THEN** it contains no functional, disabled, or placeholder Sign In, Create
  Account, or account item

## ADDED Requirements

### Requirement: Existing search and booking journey is preserved
The homepage refinement and expanded demonstration data SHALL preserve the named
flight-search route, ordinary and HTMX search behavior, flight-specific booking
entry, server-authoritative review, atomic confirmation, and receipt behavior.

#### Scenario: Visitor starts from the refined homepage
- **WHEN** the visitor follows the homepage flight action, searches a seeded route,
  selects an available seat, and submits valid passenger details
- **THEN** the existing connected booking journey can complete without a changed
  route or persistence contract
