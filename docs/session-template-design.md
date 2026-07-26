# Exercise 7: Session and Template Design

## State Handling

SkyBook uses the database for permanent information and Django sessions for temporary booking progress.

### Database Data

The following information is stored in the database:

- Cities
- Airlines
- Flights
- Seats
- Registered users
- Confirmed or cancelled bookings
- Passenger information linked to bookings
- Booking dates and statuses

### Session Data

The following information may be stored temporarily in the Django session:

- Selected origin city ID
- Selected destination city ID
- Travel date
- Travel class
- Selected flight ID
- Selected seat ID
- Temporary passenger name
- Temporary passenger email
- Current booking step

Only simple values and database IDs should be stored in the session.

Passwords, payment information, secret values, complete model objects, and permanent booking records must not be stored in the session.

After a booking is confirmed and saved in the database, the temporary booking session data should be cleared.

## Booking State Flow

1. The user enters search information.
2. Search choices are stored temporarily in the session.
3. The user selects a flight.
4. The selected flight ID is stored in the session.
5. The user selects a seat.
6. The selected seat ID is stored in the session.
7. The user enters passenger details.
8. The booking is validated and saved in the database.
9. Temporary booking data is removed from the session.

## Template Structure

All normal user-facing pages extend the shared `base.html` template.

The base template contains:

- HTML document structure
- Page title block
- Site header
- Navigation
- Message area
- Main content block
- Footer

The following pages share this layout:

- Home page
- Flight list
- Flight detail
- Booking form
- Future seat-selection page
- Future booking-confirmation page
- Future booking-history page

The `/health/` endpoint remains a plain-text response and does not use a template.