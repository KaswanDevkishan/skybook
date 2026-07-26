## ADDED Requirements

### Requirement: Accessible rendered form structure
The flight-search and guest-booking templates SHALL render every form control with its
visible Django label and SHALL preserve Django's control IDs, submitted values,
field-level errors, and error associations. Invalid bound forms SHALL expose an
accessible validation alert without changing form validation or submission behavior.

#### Scenario: Visitor opens an unbound form
- **WHEN** a visitor opens the flight-search or guest-booking page
- **THEN** every visible control has a visible label associated through the rendered
  control ID

#### Scenario: Visitor submits invalid search input
- **WHEN** a visitor submits an invalid flight search
- **THEN** the bound form retains values, renders its existing field errors, and
  exposes the validation feedback with alert semantics

#### Scenario: Visitor submits invalid booking input
- **WHEN** a visitor submits an invalid or unavailable guest booking
- **THEN** the bound form retains values, creates no booking, renders its existing
  field errors, and exposes the validation feedback with alert semantics
