## ADDED Requirements

### Requirement: Account dashboard requires authentication
The system SHALL provide an account dashboard available only to an authenticated user.
It SHALL display that user's name, email, and username and MUST redirect an anonymous
requester to sign in using a safe local next destination.

#### Scenario: Authenticated user opens account
- **WHEN** an authenticated user requests the account route
- **THEN** the response displays that user's profile fields

#### Scenario: Anonymous visitor opens account
- **WHEN** an anonymous visitor requests the account route
- **THEN** the response redirects to sign in with a local account-page next destination

### Requirement: Account history contains only active owned bookings
The account dashboard SHALL query bookings by both `user=request.user` and
`status=Confirmed` and display each matching booking's reference, flight route, departure
date, seat, and total JPY price. Confirmed future and past bookings SHALL remain visible.
It MUST NOT include Cancelled bookings, guest bookings matched only by email, or bookings
owned by another user. Cancelled filtering MUST occur in the queryset rather than only in
the template.

#### Scenario: User has owned and unrelated bookings
- **WHEN** an authenticated user opens the account page while their own, another user's,
  and guest bookings exist
- **THEN** only Confirmed bookings whose user foreign key identifies the requester are
  displayed

#### Scenario: User has confirmed and cancelled owned bookings
- **WHEN** an authenticated user opens the account page with both statuses stored
- **THEN** Confirmed bookings appear and Cancelled bookings do not render or expose
  receipt links in the main list

#### Scenario: User has no confirmed owned bookings
- **WHEN** an authenticated user has no owned bookings or all owned bookings are Cancelled
- **THEN** the page states “You have no active bookings.” and retains the Find a flight
  action

### Requirement: Owned future bookings can be cancelled without deletion
The system SHALL allow only an authenticated owner to cancel a confirmed booking before
its scheduled departure. GET SHALL display a confirmation page with the booking
reference, flight, route, departure, passenger, seat, total, a clear cancellation
warning, and notice that payment is simulated and no real refund occurs. Only a
CSRF-protected POST SHALL change status to Cancelled and redirect to My Bookings with an
accessible success message. The Booking row and all historical snapshots MUST remain.

#### Scenario: Owner cancels a future confirmed booking
- **WHEN** the authenticated owner submits the protected cancellation form before
  departure
- **THEN** status becomes Cancelled, the row and snapshots remain, and the response
  redirects to My Bookings with an accessible success message where the booking is absent

#### Scenario: Cancellation resource is not owned
- **WHEN** an anonymous user, another user, or any user with a guest or unknown reference
  requests cancellation
- **THEN** the response is 404 and exposes no booking details

#### Scenario: Cancellation is requested after departure
- **WHEN** the owner attempts to cancel after scheduled departure
- **THEN** status remains Confirmed and a clear rejection message is displayed

#### Scenario: Cancellation is repeated
- **WHEN** the owner submits cancellation for an already Cancelled booking
- **THEN** the request completes safely without changing historical data

### Requirement: Cancelled bookings release inventory
Only Confirmed bookings SHALL occupy seats. Availability queries, seat maps,
seats-remaining counts, form choices, service checks, and the database uniqueness
constraint MUST ignore Cancelled bookings so their seats can be booked again.

#### Scenario: A cancelled seat is searched and rebooked
- **WHEN** an owned booking is cancelled
- **THEN** its seat appears available, increases seats remaining, and can receive a new
  Confirmed booking while the Cancelled booking remains in history

### Requirement: My Bookings behavior depends on authentication
For an authenticated user, My Bookings SHALL lead to their account booking history. For
an anonymous visitor, My Bookings SHALL lead to a public page that clearly states guest
booking lookup is not yet available and offers appropriate onward navigation. The guest
page MUST NOT query or expose registered users' bookings.

#### Scenario: Member follows My Bookings
- **WHEN** an authenticated user activates My Bookings
- **THEN** the account booking-history destination opens

#### Scenario: Guest follows My Bookings
- **WHEN** an anonymous visitor activates My Bookings
- **THEN** a public future-lookup message opens without displaying any booking records

### Requirement: Final booking creation stores account ownership
The public authoritative atomic booking creation path SHALL require an authenticated
requester and set `Booking.user` to that requester. It MUST preserve submitted passenger
name and email independently of account profile values and MUST retain
server-authoritative pricing, reference generation, seat revalidation, and
database-backed duplicate-seat protection. Historical null-user bookings SHALL remain
unchanged and their receipts SHALL remain available.

#### Scenario: Authenticated user confirms a booking
- **WHEN** a signed-in user confirms valid passenger details for an available flight seat
- **THEN** exactly one booking is created with that user as owner and the submitted
  passenger data and authoritative amounts

#### Scenario: Guest attempts confirmation
- **WHEN** an anonymous visitor attempts to confirm valid passenger details
- **THEN** no Booking is created and authentication is required

#### Scenario: Two requesters confirm one seat
- **WHEN** stale or concurrent authenticated requests confirm the same seat
- **THEN** the database commits at most one booking and the losing request receives a
  visible availability error

### Requirement: Passenger details use editable account defaults
An authenticated user's initial unbound passenger form SHALL prefill name from their
non-empty first and last names and email from their account email. The fields SHALL remain
editable, and bound submissions, validation redisplays, review, and confirmation MUST
preserve the submitted passenger values rather than reapplying profile defaults. An
anonymous visitor SHALL receive the existing empty passenger fields.

#### Scenario: Account holder starts a booking
- **WHEN** an authenticated user with profile name and email opens a flight booking page
- **THEN** the initial passenger fields contain those account values and remain editable

#### Scenario: Account holder books for another passenger
- **WHEN** an authenticated user replaces the prefilled values and continues through
  review and confirmation
- **THEN** the edited passenger name and email are validated, displayed, and persisted
  without being overwritten by the account profile

#### Scenario: Guest starts a booking
- **WHEN** an anonymous visitor opens a flight booking page
- **THEN** passenger name and email retain empty defaults and remain editable before
  authentication

### Requirement: Passenger email is independent of account identity
Passenger email SHALL be validated only as passenger contact data. Booking forms and
views MUST NOT query registered users by passenger email, require it to match the signed-
in user's email, display “Email not registered”, or otherwise reveal whether an account
exists.

#### Scenario: Account holder books for an unregistered passenger email
- **WHEN** an authenticated user submits a syntactically valid passenger email that does
  not belong to a User
- **THEN** booking validation and completion proceed without an account-existence error

#### Scenario: Passenger email belongs to a different account
- **WHEN** an authenticated user submits a passenger email assigned to another User
- **THEN** the booking remains owned by the requester and no account-existence information
  is disclosed

### Requirement: Anonymous passenger input resumes after authentication
The anonymous seat-selection page SHALL accept seat, passenger name, and passenger email
input but replace Review price with a primary “Sign in to continue” action, a secondary
“New to SkyBook? Create an account” action, and the notice “Sign in or create an account
to continue your booking.” A valid submission SHALL store only flight, seat, passenger
name, and passenger email in a safe session payload and redirect to the selected
authentication flow using safe internal destinations.

After successful sign-in or registration, the application SHALL restore the pending
input, require the stored seat to belong to the stored flight, recheck current
availability, recalculate pricing from database values, and then allow price review. It
MUST NOT store submitted prices, passwords, payment data, or arbitrary redirect URLs.

#### Scenario: Anonymous visitor chooses sign in
- **WHEN** an anonymous visitor submits valid seat and passenger details with Sign in to
  continue
- **THEN** the safe pending fields are stored, no Booking exists, and the response
  redirects to Sign In with a local resume destination

#### Scenario: Anonymous visitor chooses registration
- **WHEN** an anonymous visitor submits valid seat and passenger details with Create
  account
- **THEN** the same safe pending fields are stored, no Booking exists, and the response
  redirects to Create Account with a local resume destination

#### Scenario: Authentication resumes an available seat
- **WHEN** sign-in or registration succeeds with valid pending data for an available seat
- **THEN** the passenger values are restored and current database pricing is displayed
  for review

#### Scenario: Pending seat no longer exists or is unavailable
- **WHEN** resume finds a missing flight or seat, a seat outside the flight, or a newly
  occupied seat
- **THEN** invalid identifiers are cleared, no Booking is created, and the user receives
  a safe availability response

### Requirement: Pending booking session data is cleaned up
Pending booking data SHALL be cleared after successful confirmation. Malformed pending
data and data referencing a missing flight or seat MUST be cleared when detected.

#### Scenario: Owned booking confirms successfully
- **WHEN** an authenticated user completes confirmation from pending or reviewed data
- **THEN** the Booking belongs to that user and pending booking session data is removed

#### Scenario: Pending identifiers are invalid
- **WHEN** pending data cannot identify an existing flight-scoped seat
- **THEN** the pending session key is removed without exposing account or booking data

### Requirement: Owned booking details are access controlled
An authenticated booking receipt or detail SHALL be retrievable only by its owning user.
An anonymous requester or a different authenticated user MUST receive status 404 for that
booking reference. A null-user guest booking receipt SHALL remain available through its
existing high-entropy reference so guest confirmation continues to work.

#### Scenario: Owner opens receipt
- **WHEN** an authenticated owner requests their booking reference
- **THEN** the response displays the booking receipt

#### Scenario: Owner opens a cancelled receipt directly
- **WHEN** an authenticated owner requests the reference of their Cancelled booking
- **THEN** the response displays the retained receipt even though My Bookings does not
  link to it

#### Scenario: Another user guesses receipt reference
- **WHEN** an authenticated non-owner or anonymous visitor requests a user-owned booking
  reference
- **THEN** the response has status 404 and exposes no booking details

#### Scenario: Guest follows confirmation redirect
- **WHEN** an anonymous guest requests the reference of their null-user booking
- **THEN** the existing guest receipt is displayed
