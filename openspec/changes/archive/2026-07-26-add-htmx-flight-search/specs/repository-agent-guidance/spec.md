## MODIFIED Requirements

### Requirement: Current exercise scope boundary
Repository guidance SHALL identify the current work as Exercise 10 and SHALL permit one
server-driven HTMX flight-search interaction, a reusable result partial, accessible
loading and live-region feedback, and their tests and documentation in addition to the
existing Django foundation, schema, administration, basic views, validated GET flight
search, POST guest booking creation, and Exercise 9 semantic, responsive, accessible
interface. It SHALL continue to prohibit authentication screens, payments, an
interactive seat-map interface, checkout, external airline APIs, production styling,
other client-side frameworks, and a complete booking workflow. It SHALL direct
contributors not to add seat class or another schema field unless a later requirement
genuinely requires it.

#### Scenario: Exercise 10 HTMX feature is requested
- **WHEN** an agent prepares the specified server-driven flight-result update
- **THEN** repository guidance identifies that focused interaction as permitted within
  Exercise 10

#### Scenario: Existing search or booking work is reviewed
- **WHEN** an agent changes the presentation or response representation of flight search
- **THEN** repository guidance requires the existing validation, GET fallback,
  persistence, and database-backed duplicate-seat behavior to remain intact

#### Scenario: Deferred feature is requested
- **WHEN** a requested task would add authentication UI, payments, an interactive seat
  map, checkout, an external airline integration, production styling, another
  client-side framework, or a complete booking workflow
- **THEN** the guidance identifies that work as outside the Exercise 10 scope
