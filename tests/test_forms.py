from datetime import timedelta

import pytest
from django.utils import timezone
from reservations.forms import BookingForm, FlightSearchForm
from reservations.models import Airline, Booking, City, Flight, Seat


@pytest.fixture
def cities(db):
    return (
        City.objects.create(name="Tokyo", code="TYO"),
        City.objects.create(name="Osaka", code="OSA"),
    )


@pytest.fixture
def seat(db, cities):
    origin, destination = cities
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    departure = timezone.now() + timedelta(days=1)
    flight = Flight.objects.create(
        airline=airline,
        flight_number="101",
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=1),
    )
    return Seat.objects.create(flight=flight, seat_number="1A")


def test_flight_search_form_accepts_distinct_cities_and_valid_date(cities):
    origin, destination = cities
    form = FlightSearchForm(
        {
            "origin": origin.pk,
            "destination": destination.pk,
            "departure_date": "2026-08-01",
        }
    )

    assert form.is_valid()


def test_flight_search_form_rejects_same_origin_and_destination(cities):
    origin, _ = cities
    form = FlightSearchForm(
        {
            "origin": origin.pk,
            "destination": origin.pk,
            "departure_date": "2026-08-01",
        }
    )

    assert not form.is_valid()
    assert "Origin and destination must be different." in form.non_field_errors()


def test_booking_form_accepts_valid_email(seat):
    form = BookingForm(
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        }
    )

    assert form.is_valid()


def test_booking_form_rejects_invalid_email(seat):
    form = BookingForm(
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "not-an-email",
        }
    )

    assert not form.is_valid()
    assert "passenger_email" in form.errors


def test_booking_form_rejects_already_booked_seat(seat):
    Booking.objects.create(
        seat=seat,
        guest_name="Existing Passenger",
        guest_email="existing@example.com",
    )
    form = BookingForm(
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        }
    )

    assert not form.is_valid()
    assert "This seat is already booked." in form.errors["seat"]


def test_booking_form_save_maps_passenger_fields_to_guest_fields(seat):
    form = BookingForm(
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        }
    )

    assert form.is_valid()
    booking = form.save()

    assert booking.seat == seat
    assert booking.user is None
    assert booking.guest_name == "Aiko Tanaka"
    assert booking.guest_email == "aiko@example.com"
