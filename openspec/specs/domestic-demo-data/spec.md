# Domestic Demonstration Data Specification

## Purpose

Define representative Japanese destination, route, schedule, seat, and preservation
requirements for SkyBook's idempotent demonstration-data seeding.

## Requirements

### Requirement: Major Japanese destination catalog
The demonstration seed catalog SHALL contain approximately 30–40 major Japanese
domestic airports or airport-served destinations across Hokkaido, Tohoku, Kanto,
Chubu, Kansai, Chugoku, Shikoku, Kyushu, and Okinawa. Every entry MUST use a stable,
unique airport code and a clear English name. The catalog SHALL be documented as
representative demonstration data, not a complete airport directory.

#### Scenario: Empty database receives destination coverage
- **WHEN** `seed_demo_data` runs on an empty migrated database
- **THEN** approximately 30–40 uniquely coded destinations are available and every
  required Japanese region is represented

#### Scenario: Destination catalog is inspected
- **WHEN** a contributor reviews the seed definitions and README
- **THEN** entries have stable unique codes and clear English names and the dataset is
  identified as incomplete demonstration data

### Requirement: Existing destinations are preserved
The seed command MUST preserve every existing `City` row, primary key, code, name, and
relationship. It SHALL create a missing catalog destination by stable code and SHALL
NOT rename, replace, delete, or merge an existing destination.

#### Scenario: Existing catalog destination has persisted data
- **WHEN** a destination with a catalog code already exists before seeding
- **THEN** the command retains that row's identifier and persisted fields

#### Scenario: Existing flight references a destination
- **WHEN** a seeded or unrelated flight references an existing destination
- **THEN** repeated seeding leaves the referenced destination and relationship intact

### Requirement: Curated valid domestic routes
The seed catalog SHALL define a bounded set of realistic demonstration routes with
enough flights for meaningful origin and destination selection. Routes MUST reference
catalog destination codes, use distinct origins and destinations, have stable unique
flight identities, arrive after departure, and collectively involve all required
Japanese regions. The catalog SHALL NOT claim to represent every route or a live
aviation schedule.

#### Scenario: Seed route catalog is valid
- **WHEN** the configured routes are validated
- **THEN** every endpoint exists, every origin differs from its destination, every
  duration is positive, flight identities are unique, and all required regions occur

#### Scenario: Visitor searches demonstration routes
- **WHEN** seeding completes and a visitor opens flight search
- **THEN** multiple valid regional origin and destination relationships are available
  through the existing search controls

### Requirement: Seeded schedules are creation-time only
The command SHALL calculate a future schedule only when a catalog flight is initially
created. A later or repeated run MUST NOT change an existing flight's origin,
destination, departure time, or arrival time, even when the original schedule is no
longer future.

#### Scenario: Missing flight is initially seeded
- **WHEN** a catalog flight does not exist
- **THEN** it is created with a valid future departure and later arrival relative to
  that run

#### Scenario: Deployment date advances
- **WHEN** the command runs again on a later date
- **THEN** every existing catalog flight retains its original endpoints and schedule

### Requirement: Seeded seats are complete and idempotent
Every newly seeded flight SHALL receive the established Economy and Business seat
structures, Window/Middle/Aisle types, and positive whole-yen JPY prices. Seat identity
MUST remain unique by flight and seat number. Repeated seeding SHALL create missing
catalog seats without duplicating, repricing, or reclassifying existing seats.

#### Scenario: New flight receives seats
- **WHEN** the command initially creates a catalog flight
- **THEN** that flight has bookable Economy and Business seats covering the established
  seat types and JPY pricing

#### Scenario: Seed command is repeated
- **WHEN** the command runs after its flights and seats already exist
- **THEN** no seat is duplicated and every existing seat identity, classification, and
  price remains unchanged

### Requirement: Bookings are outside seed mutation
The demonstration seed command MUST NOT create, update, or delete a `Booking` and MUST
retain the database-backed one-booking-per-seat invariant.

#### Scenario: Existing booking survives repeated seeding
- **WHEN** a seat has a guest or registered-user booking before the command runs
- **THEN** the booking and all of its persisted fields remain unchanged

#### Scenario: Missing demo records are added around a booking
- **WHEN** a database contains an existing booking and lacks newer catalog destinations
  or flights
- **THEN** the command adds only missing demo records without affecting the booking
