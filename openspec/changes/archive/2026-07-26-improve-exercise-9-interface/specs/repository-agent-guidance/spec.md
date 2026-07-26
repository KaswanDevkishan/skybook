## MODIFIED Requirements

### Requirement: Current exercise scope boundary
Repository guidance SHALL identify the current work as Exercise 9 and SHALL permit
clean semantic HTML, external CSS, responsive design, accessibility improvements, and
their tests and documentation in addition to the existing Django foundation, schema,
administration, basic views, validated GET flight search, and POST guest booking
creation. It SHALL continue to prohibit authentication screens, payments, an
interactive seat-map interface, external airline APIs, production styling, and a
complete booking workflow. It SHALL direct contributors not to add seat class or
another schema field unless a later requirement genuinely requires it.

#### Scenario: Exercise 9 interface feature is requested
- **WHEN** an agent prepares semantic template, external CSS, responsive layout, or
  accessibility work for the existing public pages
- **THEN** repository guidance identifies that focused work as permitted within
  Exercise 9

#### Scenario: Existing search or booking work is reviewed
- **WHEN** an agent changes the presentation of the search or guest-booking forms
- **THEN** repository guidance requires the existing validation, request, persistence,
  and database-backed duplicate-seat behavior to remain intact

#### Scenario: Deferred feature is requested
- **WHEN** a requested task would add authentication UI, payments, an interactive
  seat map, an external airline integration, production styling, or a complete booking
  workflow
- **THEN** the guidance identifies that work as outside the Exercise 9 scope
