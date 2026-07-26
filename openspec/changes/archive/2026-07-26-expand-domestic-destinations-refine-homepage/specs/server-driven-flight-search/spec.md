## ADDED Requirements

### Requirement: Expanded domestic data retains the search contract
The ordinary and `HX-Request: true` flight searches SHALL expose the same expanded
destination choices and SHALL filter seeded flights by exact validated origin,
destination, and departure date without changing the reusable results partial,
ordering, accessibility feedback, or connected booking actions.

#### Scenario: Visitor selects an expanded destination
- **WHEN** a catalog destination participates in a seeded flight
- **THEN** the existing search form offers it as a valid origin or destination choice

#### Scenario: Ordinary and enhanced searches use expanded data
- **WHEN** equivalent valid searches are submitted with and without
  `HX-Request: true`
- **THEN** both representations return the same matching seeded flights in departure
  order through their existing full-page and partial contracts

#### Scenario: Expanded route has no matching date
- **WHEN** a visitor submits valid expanded origin and destination values for a date
  without a matching seeded flight
- **THEN** the existing explicit empty state is returned without changing search
  controls or creating data
