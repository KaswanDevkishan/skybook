# Django Project Foundation Specification

## Purpose

Define SkyBook's runnable Django foundation, SQLite development environment, admin
integration, quality workflow, and current course-exercise feature boundary.

## Requirements

### Requirement: Runnable generated Django project
SkyBook SHALL run as a Django project created with `django-admin`, and its main
`reservations` application SHALL be created with `manage.py startapp`.

#### Scenario: Development server starts
- **WHEN** a contributor installs the documented dependencies and runs the documented
  Django development command
- **THEN** Django starts with the SkyBook settings without importing Flask

#### Scenario: Main application is installed
- **WHEN** Django loads the project settings
- **THEN** the generated `reservations` application is present in the installed
  applications

### Requirement: SQLite development database
The Django development configuration SHALL use SQLite and SHALL keep local database
files out of version control.

#### Scenario: Clean development database is initialized
- **WHEN** a contributor applies migrations without overriding database configuration
- **THEN** Django creates or updates a local SQLite database

### Requirement: Administrative model access
The Django administrative site SHALL register `City`, `Airline`, `Flight`, `Seat`, and
`Booking`.

#### Scenario: Administrator inspects domain records
- **WHEN** an authenticated staff user opens the Django admin site
- **THEN** each SkyBook domain model is available for administration

### Requirement: Reproducible framework quality workflow
Project configuration and CI SHALL provide documented `uv`, Ruff, Pytest, coverage,
and Django migration-check commands that work with the generated Django structure.

#### Scenario: Contributor runs verification
- **WHEN** a contributor follows the documented verification commands
- **THEN** formatting, linting, model tests, coverage, and migration drift checks run
  against the Django project

### Requirement: Deferred product features
The Django course project SHALL provide its foundation, administrative model access,
reservation schema, tests, basic public views, and the explicitly bounded Exercise 8
flight-search and guest booking forms. Exercise 8 SHALL permit validated GET
filtering by origin, destination, and departure date plus CSRF-protected POST
creation of a guest booking for an existing available seat. It SHALL NOT provide
seat-class search without model support, authentication screens, payments, an
interactive seat map, external airline APIs, production styling, or a complete
multi-step booking workflow.

#### Scenario: Exercise 8 application scope is reviewed
- **WHEN** a contributor inspects the routes, templates, forms, and application
  services
- **THEN** the application contains the permitted foundation, schema, basic views,
  validated flight search, and simple guest booking behavior without the deferred
  features

#### Scenario: Visitor submits the booking form
- **WHEN** valid guest and available-seat data is submitted with POST and CSRF
  protection
- **THEN** the application creates one guest booking and redirects without starting
  a payment, authentication, seat-map, or multi-step workflow

### Requirement: Obsolete Flask runtime removal
The repository SHALL NOT retain Flask as a runtime dependency or expose the obsolete
Flask application entry point.

#### Scenario: Framework replacement is verified
- **WHEN** a contributor searches runtime dependencies and entry points
- **THEN** the project uses Django without an active Flask scaffold
