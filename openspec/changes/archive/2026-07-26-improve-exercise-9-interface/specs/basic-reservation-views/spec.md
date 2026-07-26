## ADDED Requirements

### Requirement: Semantic public view presentation
The existing home, flight-list, flight-detail, and booking-form views SHALL render
their content with page-appropriate semantic HTML while preserving their named routes,
request methods, context values, form actions, response statuses, search results, and
booking outcomes.

#### Scenario: Visitor opens the home page
- **WHEN** a visitor sends GET `/`
- **THEN** the response presents the welcome content and destination links in semantic
  page regions without changing either link target

#### Scenario: Visitor views flight results
- **WHEN** a visitor sends GET `/flights/`
- **THEN** the search form and flight-result or empty-state content use appropriate
  semantic elements without changing search behavior

#### Scenario: Visitor views a flight
- **WHEN** a visitor opens an existing flight detail URL
- **THEN** the response presents the existing airline, route, departure, and arrival
  values in an appropriately labeled content region

#### Scenario: Visitor books a flight
- **WHEN** a visitor opens or submits the booking form
- **THEN** the form retains its POST action, CSRF protection, fields, validation, and
  persistence behavior within the improved semantic presentation
