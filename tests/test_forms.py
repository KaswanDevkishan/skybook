from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from reservations.forms import BookingForm, FlightSearchForm
from reservations.models import Airline, Booking, City, Flight, Seat


@pytest.fixture
def route(db):
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    return origin, destination, airline


@pytest.fixture
def flight(route):
    origin, destination, airline = route
    departure = timezone.now() + timedelta(days=1)
    return Flight.objects.create(
        airline=airline,
        flight_number="101",
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=1),
    )


@pytest.fixture
def seat(flight):
    return Seat.objects.create(
        flight=flight,
        seat_number="1A",
        cabin_class=Seat.CabinClass.BUSINESS,
        seat_type=Seat.SeatType.WINDOW,
        price=Decimal("50000"),
    )


def test_flight_search_form_accepts_distinct_cities_and_valid_date(route):
    origin, destination, _ = route
    form = FlightSearchForm(
        {
            "origin": origin.pk,
            "destination": destination.pk,
            "departure_date": "2026-08-01",
        }
    )

    assert form.is_valid()


def test_flight_search_form_rejects_same_origin_and_destination(route):
    origin, _, _ = route
    form = FlightSearchForm(
        {
            "origin": origin.pk,
            "destination": origin.pk,
            "departure_date": "2026-08-01",
        }
    )

    assert not form.is_valid()
    assert "Origin and destination must be different." in form.non_field_errors()


def test_booking_form_is_scoped_to_available_seats_on_selected_flight(flight, seat):
    other_flight = Flight.objects.create(
        airline=flight.airline,
        flight_number="102",
        origin=flight.origin,
        destination=flight.destination,
        departure_time=flight.departure_time + timedelta(days=1),
        arrival_time=flight.arrival_time + timedelta(days=1),
    )
    other_seat = Seat.objects.create(flight=other_flight, seat_number="1A")
    booked_seat = Seat.objects.create(flight=flight, seat_number="1B")
    Booking.objects.create(
        seat=booked_seat,
        guest_name="Booked Guest",
        guest_email="booked@example.com",
    )

    form = BookingForm(flight=flight)

    assert list(form.fields["seat"].queryset) == [seat]
    assert other_seat not in form.fields["seat"].queryset
    assert booked_seat not in form.fields["seat"].queryset


def test_booking_form_accepts_valid_passenger_and_scoped_seat(flight, seat):
    form = BookingForm(
        {
            "seat": seat.pk,
            "passenger_name": "  Aiko Tanaka  ",
            "passenger_email": "aiko@example.com",
        },
        flight=flight,
    )

    assert form.is_valid()
    assert form.cleaned_data["passenger_name"] == "Aiko Tanaka"


def test_booking_form_rejects_invalid_email(flight, seat):
    form = BookingForm(
        {
            "seat": seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "not-an-email",
        },
        flight=flight,
    )

    assert not form.is_valid()
    assert "passenger_email" in form.errors


def test_booking_form_rejects_cross_flight_injection(flight, route):
    origin, destination, airline = route
    departure = timezone.now() + timedelta(days=3)
    other_flight = Flight.objects.create(
        airline=airline,
        flight_number="999",
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=1),
    )
    other_seat = Seat.objects.create(flight=other_flight, seat_number="9A")
    form = BookingForm(
        {
            "seat": other_seat.pk,
            "passenger_name": "Aiko Tanaka",
            "passenger_email": "aiko@example.com",
        },
        flight=flight,
    )

    assert not form.is_valid()
    assert "Select an available seat for this flight." in form.errors["seat"]
