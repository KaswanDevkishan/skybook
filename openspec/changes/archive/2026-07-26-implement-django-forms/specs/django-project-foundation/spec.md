## MODIFIED Requirements

### Requirement: Deferred product features
The Django course project SHALL provide its foundation, administrative model access, reservation
schema, tests, basic public views, and the explicitly bounded Exercise 8 flight-search and guest
booking forms. Exercise 8 SHALL permit validated GET filtering by origin, destination, and
departure date plus CSRF-protected POST creation of a guest booking for an existing available
seat. It SHALL NOT provide seat-class search without model support, authentication screens,
payments, an interactive seat map, external airline APIs, production styling, or a complete
multi-step booking workflow.

#### Scenario: Exercise 8 application scope is reviewed
- **WHEN** a contributor inspects the routes, templates, forms, and application services
- **THEN** the application contains the permitted foundation, schema, basic views, validated flight search, and simple guest booking behavior without the deferred features

#### Scenario: Visitor submits the booking form
- **WHEN** valid guest and available-seat data is submitted with POST and CSRF protection
- **THEN** the application creates one guest booking and redirects without starting a payment, authentication, seat-map, or multi-step workflow
