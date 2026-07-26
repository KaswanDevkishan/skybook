# Reservation Data Model Specification

## Purpose

Define the initial SkyBook airline reservation entities, relationships, display
representations, and database-backed integrity constraints.

## Requirements

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

### Requirement: Airline records
The system SHALL persist airlines with a name and a unique short code and SHALL provide
a useful human-readable string representation.

#### Scenario: Duplicate airline code is rejected
- **WHEN** two airlines are saved with the same normalized code
- **THEN** the database rejects the duplicate

#### Scenario: Airline is displayed
- **WHEN** an airline is converted to text
- **THEN** the result identifies the airline by its name and code

### Requirement: Flight schedule records
The system SHALL persist each flight with an airline, flight number, origin city,
destination city, departure time, and arrival time. A flight MUST have distinct
origin and destination cities, MUST arrive after it departs, and MUST be unique for
its scheduled identity.

#### Scenario: Valid flight is persisted
- **WHEN** a flight has distinct cities, increasing times, and a new scheduled identity
- **THEN** the database stores the flight and its relationships

#### Scenario: Same-city flight is rejected
- **WHEN** a flight uses the same city as its origin and destination
- **THEN** the database rejects the flight

#### Scenario: Non-increasing flight time is rejected
- **WHEN** a flight arrives at or before its departure time
- **THEN** the database rejects the flight

#### Scenario: Duplicate scheduled flight is rejected
- **WHEN** a second flight uses the same airline, flight number, and departure time
- **THEN** the database rejects the duplicate scheduled identity

#### Scenario: Flight is displayed
- **WHEN** a flight is converted to text
- **THEN** the result identifies its airline code and flight number

### Requirement: Seats belong to flights
The system SHALL persist seats for a flight and SHALL require each seat number to be
unique within that flight.

#### Scenario: Same seat number on different flights is accepted
- **WHEN** two flights each define a seat with the same seat number
- **THEN** the database stores both seats

#### Scenario: Duplicate seat within a flight is rejected
- **WHEN** the same flight receives two seats with the same seat number
- **THEN** the database rejects the duplicate

#### Scenario: Seat is displayed
- **WHEN** a seat is converted to text
- **THEN** the result identifies both the flight and seat number

### Requirement: Registered and guest bookings
The system SHALL persist a booking for a seat and SHALL allow its built-in
authentication user reference to be null for a guest booking. A booking MUST retain
guest contact fields that can identify a guest when no user is associated.

#### Scenario: Registered user booking is persisted
- **WHEN** a booking references a seat and a Django authentication user
- **THEN** the database stores the booking and user relationship

#### Scenario: Guest booking is persisted
- **WHEN** a booking references a seat, has no user, and contains guest contact data
- **THEN** the database stores the booking with a null user

#### Scenario: Booking survives user deletion
- **WHEN** the user associated with a booking is deleted
- **THEN** the booking remains and its user reference becomes null

#### Scenario: Booking is displayed
- **WHEN** a booking is converted to text
- **THEN** the result identifies the booked seat and registered user or guest

### Requirement: A flight seat cannot be booked twice
The system MUST enforce in the database that at most one booking references a given
flight seat, independent of browser state or model-form validation.

#### Scenario: Duplicate booking is rejected
- **WHEN** a stale or concurrent request attempts to create a second booking for an
  already-booked seat
- **THEN** the database rejects the second booking
