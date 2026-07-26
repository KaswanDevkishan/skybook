## ADDED Requirements

### Requirement: Account registration uses Django authentication
The system SHALL provide a CSRF-protected Create Account form collecting username, email,
first name, last name, password, and password confirmation. It MUST use Django's built-in
user model, password hashing, and configured password validators; it MUST NOT store, log,
or render a submitted password as plain text. A successful registration SHALL create one
user, establish a Django authenticated session, and redirect to the account page.

#### Scenario: Visitor creates an account
- **WHEN** a visitor submits valid unique account details and matching acceptable passwords
- **THEN** one built-in Django user is created with a hashed password, the visitor is
  authenticated, and the response redirects to the account page

#### Scenario: Password is invalid
- **WHEN** a visitor submits mismatched passwords or a password rejected by a configured
  Django validator
- **THEN** registration creates no user and presents accessible validation feedback without
  redisplaying either password value

### Requirement: Registration identifiers are validated
Registration MUST enforce Django's unique-username behavior, validate email syntax, and
reject an email already assigned to an account using case-insensitive comparison. Invalid
registration SHALL retain safe non-password fields and SHALL expose no account-existence
information beyond ordinary Create Account field validation.

#### Scenario: Username already exists
- **WHEN** a visitor submits a username already used by another user
- **THEN** no new user is created and the username field has an accessible error

#### Scenario: Email is malformed
- **WHEN** a visitor submits a value that fails Django email validation
- **THEN** no new user is created and the email field has an accessible error

#### Scenario: Email already exists with different letter case
- **WHEN** a visitor submits an email equal case-insensitively to an existing account email
- **THEN** no new user is created and registration displays ordinary field validation

### Requirement: Sign in uses Django sessions
The system SHALL provide a CSRF-protected sign-in form using Django authentication and
sessions. Valid username and password credentials SHALL establish an authenticated
session; invalid credentials SHALL create no session and SHALL return generic accessible
authentication feedback that does not disclose unrelated account data.

#### Scenario: User signs in successfully
- **WHEN** a user submits a valid username and password
- **THEN** Django authenticates the session and redirects to the safe requested destination
  or the account fallback

#### Scenario: Credentials fail
- **WHEN** a visitor submits an invalid username and password combination
- **THEN** the visitor remains anonymous and one alert with `role="alert"` says
  “We couldn’t sign you in. Check your username and password and try again.” without
  duplicating Django's raw non-field authentication error

### Requirement: Authentication redirects are safe
Authentication views SHALL accept a `next` destination only when Django determines it is
safe for the current host and request scheme. Missing, malformed, protocol-relative,
cross-host, or otherwise unsafe destinations MUST fall back to a fixed local route.
Successful sign-in or registration with a valid pending booking SHALL use the fixed local
booking-resume destination.

#### Scenario: Local next destination is supplied
- **WHEN** a user signs in with an allowed same-host local `next` URL
- **THEN** the response redirects to that local destination

#### Scenario: External next destination is supplied
- **WHEN** a user signs in with a cross-host or protocol-relative `next` URL
- **THEN** the response ignores it and redirects to the fixed account fallback

#### Scenario: Authentication completes with pending booking data
- **WHEN** sign-in or registration succeeds while the session contains a valid pending
  booking
- **THEN** the response redirects to the fixed local booking-resume destination

### Requirement: Sign out is a protected state change
The system SHALL sign a user out only through a CSRF-protected POST action. A GET request
MUST NOT terminate the session, and a successful POST SHALL clear the Django authenticated
session and redirect to a fixed public route.

#### Scenario: User posts log out
- **WHEN** an authenticated user submits the navigation Log Out form with a valid CSRF token
- **THEN** Django ends the authenticated session and redirects to the fixed public route

#### Scenario: Caller requests log out with GET
- **WHEN** a caller sends GET to the logout endpoint
- **THEN** the endpoint rejects the method and does not log out an authenticated user

#### Scenario: Logout POST omits CSRF
- **WHEN** a client with CSRF checks enforced posts to logout without a valid token
- **THEN** Django returns status 403 and retains the authenticated session

### Requirement: Shared navigation reflects authentication state
Every complete HTML page SHALL render the SkyBook brand as a `/flights/` link and a usable
primary navigation whose entries reflect `request.user.is_authenticated`. Logged-out
navigation SHALL contain Flights, My Bookings, Sign In, and Create Account. Logged-in
navigation SHALL contain Flights, My Bookings, Account, and a POST Log Out action, and
MUST NOT show Sign In or Create Account. Current destinations SHALL expose an active state
where practical.

#### Scenario: Anonymous visitor reads navigation
- **WHEN** an anonymous visitor opens a complete page
- **THEN** the brand links to flight search and the logged-out navigation entries are present without
  fake or disabled authentication links

#### Scenario: Authenticated user reads navigation
- **WHEN** an authenticated user opens a complete page
- **THEN** the brand links to flight search and the logged-in navigation entries and POST Log Out action
  are present
