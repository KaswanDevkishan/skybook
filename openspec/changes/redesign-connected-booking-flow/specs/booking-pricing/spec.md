## ADDED Requirements

### Requirement: Authoritative whole-yen pricing
The system SHALL represent base fare, taxes and fees, and total price as Decimal
whole-yen JPY amounts. Taxes and fees MUST equal 10% of base fare rounded to the
nearest whole yen with `ROUND_HALF_UP`, and total price MUST equal base fare plus
taxes and fees.

#### Scenario: Price is calculated
- **WHEN** a seat has a base fare of JPY 15,005
- **THEN** the authoritative calculation returns JPY 1,501 taxes and fees and a JPY
  16,506 total

#### Scenario: Browser supplies different amounts
- **WHEN** a booking submission contains missing or manipulated browser price values
- **THEN** the server ignores those values and calculates all confirmed amounts from
  the selected seat's persisted price

### Requirement: Confirmed prices are immutable snapshots
The system MUST copy the authoritative base fare, taxes and fees, and total price onto
the `Booking` when confirmation succeeds and MUST use those stored values for all
historical booking displays.

#### Scenario: Seat price later changes
- **WHEN** a seat's current price changes after its booking was confirmed
- **THEN** the booking confirmation continues to display the original stored amounts

### Requirement: Booking references are readable and unique
Each booking MUST receive a non-empty uppercase reference with a `SKY-` prefix and a
random human-readable suffix, and the database MUST enforce reference uniqueness.
Reference generation SHALL retry a bounded number of reference collisions without
weakening the one-booking-per-seat invariant.

#### Scenario: Booking is confirmed
- **WHEN** a new booking is successfully persisted
- **THEN** it has a user-friendly reference that is unique among bookings

#### Scenario: Generated reference collides
- **WHEN** a candidate reference already belongs to another booking
- **THEN** creation retries with a new candidate and does not alter the existing
  booking

