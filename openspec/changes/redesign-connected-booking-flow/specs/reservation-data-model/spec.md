## MODIFIED Requirements

### Requirement: Seats belong to flights
The system SHALL persist seats for a flight and SHALL require each seat number to be
unique within that flight. Every seat MUST have a cabin class chosen from Economy or
Business, a seat type chosen from Window, Middle, or Aisle, and a non-negative
Decimal whole-yen JPY price.

#### Scenario: Same seat number on different flights is accepted
- **WHEN** two flights each define a seat with the same seat number
- **THEN** the database stores both seats

#### Scenario: Duplicate seat within a flight is rejected
- **WHEN** the same flight receives two seats with the same seat number
- **THEN** the database rejects the duplicate

#### Scenario: Classified priced seat is persisted
- **WHEN** a seat has valid cabin, type, and Decimal JPY price values
- **THEN** the database stores its classification and price

#### Scenario: Seat is displayed
- **WHEN** a seat is converted to text
- **THEN** the result identifies both the flight and seat number

### Requirement: Registered and guest bookings
The system SHALL persist a booking for a seat and SHALL allow its built-in
authentication user reference to be null for a guest booking. A booking MUST retain
guest contact fields that identify a guest when no user is associated. It MUST also
store Decimal whole-yen base fare, taxes and fees, and total price snapshots, a unique
booking reference, and a creation timestamp.

#### Scenario: Registered user booking is persisted
- **WHEN** a booking references a seat and a Django authentication user
- **THEN** the database stores the booking and user relationship

#### Scenario: Guest booking is persisted
- **WHEN** a booking references a seat, has no user, and contains guest contact data
- **THEN** the database stores the booking with a null user

#### Scenario: Booking survives user deletion
- **WHEN** the user associated with a booking is deleted
- **THEN** the booking remains and its user reference becomes null

#### Scenario: Booking retains confirmation data
- **WHEN** a booking is created with authoritative amounts and a reference
- **THEN** those amounts, its unique reference, and its creation time remain stored on
  the booking independently of later seat changes

#### Scenario: Booking is displayed
- **WHEN** a booking is converted to text
- **THEN** the result identifies the booking reference and registered user or guest

## ADDED Requirements

### Requirement: Pricing migration preserves reservation data
The schema migration SHALL populate valid classification and price values for every
existing seat and valid immutable price and reference values for every existing
booking before final non-null and unique constraints are enforced. It MUST NOT delete
or disconnect existing seats or bookings.

#### Scenario: Prior schema contains existing bookings
- **WHEN** the new migration is applied
- **THEN** each existing row remains related to the same flight and seat and receives
  deterministic safe pricing plus a unique booking reference

#### Scenario: Migration runs on supported databases
- **WHEN** migrations are applied to local SQLite or production PostgreSQL
- **THEN** the resulting schema and constraints support the same reservation behavior

