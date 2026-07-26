## ADDED Requirements

### Requirement: Accessible dynamic flight-result status
The flight-search page SHALL expose its targeted result region as a polite live update
and SHALL provide a textual loading status associated with enhanced requests. The
loading state SHALL remain understandable without relying on motion or color, and
updated flight links and controls SHALL retain visible focus and keyboard usability.

#### Scenario: Flight results are loading
- **WHEN** an enhanced flight-search request is in progress
- **THEN** a visible textual status communicates that flights are loading and is
  exposed to assistive technology

#### Scenario: Flight-result contents are replaced
- **WHEN** an enhanced response replaces the contents of the flight-results region
- **THEN** the node that owns the polite live-region semantics remains connected,
  assistive technology can discover the non-disruptive result update, and all result
  links remain keyboard operable

#### Scenario: Enhanced validation fails
- **WHEN** an enhanced flight search returns invalid form feedback
- **THEN** the result update visibly identifies the validation problem with alert
  semantics while retaining the existing labeled form controls
