## MODIFIED Requirements

### Requirement: City records
The system SHALL persist cities with a name and a unique normalized short code and
SHALL provide a useful human-readable string representation. Demonstration seeding
MUST treat the stable code as identity and MUST preserve every existing city row,
identifier, persisted name, and flight relationship.

#### Scenario: Duplicate city code is rejected
- **WHEN** two cities are saved with the same normalized code
- **THEN** the database rejects the duplicate

#### Scenario: City is displayed
- **WHEN** a city is converted to text
- **THEN** the result identifies the city by its name and code

#### Scenario: Existing city is encountered during seeding
- **WHEN** the seed catalog contains the code of an existing city
- **THEN** seeding reuses the existing row without renaming or replacing it
