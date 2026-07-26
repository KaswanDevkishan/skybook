## MODIFIED Requirements

### Requirement: Shared semantic page structure
Every rendered reservation page SHALL provide a skip-to-content link whose target is a
stable main-content ID, a header, an understandably named primary navigation landmark,
and one main landmark. The shared layout SHALL NOT render a site footer. Page content
SHALL use semantic sections, articles, forms, and headings where appropriate, maintain
a logical heading hierarchy, and avoid presentation-only wrappers.

#### Scenario: Visitor navigates page landmarks
- **WHEN** a visitor opens any reservation HTML page
- **THEN** the response contains the header, named navigation, main landmark, and skip
  link targeting the stable main-content element and contains no footer landmark

#### Scenario: Visitor reads page structure
- **WHEN** a visitor or assistive technology traverses a reservation page
- **THEN** headings and page-specific semantic elements describe the content in a
  logical order

#### Scenario: Contributor reviews shared presentation
- **WHEN** the footer is removed from the shared template
- **THEN** footer-only styles and footer-specific tests are absent while other shared
  accessibility and responsive rules remain covered
