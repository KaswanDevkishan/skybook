## MODIFIED Requirements

### Requirement: Current exercise scope boundary
Repository guidance SHALL identify the current work as Exercise 8 and SHALL permit proper Django
forms for GET flight search and POST guest booking creation in addition to the existing Django
foundation, schema, administration, and basic views. It SHALL continue to prohibit authentication
screens, payments, an interactive seat-map interface, external airline APIs, production styling,
and a complete booking workflow. It SHALL direct contributors not to add seat class or another
schema field unless a later requirement genuinely requires it.

#### Scenario: Exercise 8 form feature is requested
- **WHEN** an agent prepares validated flight search or simple guest booking form work
- **THEN** repository guidance identifies that focused work as permitted within Exercise 8

#### Scenario: Deferred feature is requested
- **WHEN** a requested task would add authentication UI, payments, an interactive seat map, an external airline integration, or a complete booking workflow
- **THEN** the guidance identifies that work as outside the Exercise 8 scope
