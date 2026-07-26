from datetime import UTC, datetime, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.test import override_settings
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
    assert form.non_field_errors() == [
        "Your origin and destination cannot be the same. Please select a different airport."
    ]
    assert form.fields["origin"].widget.attrs["aria-invalid"] == "true"
    assert form.fields["destination"].widget.attrs["aria-invalid"] == "true"
    assert form.fields["origin"].widget.attrs["aria-describedby"] == "same-route-error"
    assert form.fields["destination"].widget.attrs["aria-describedby"] == "same-route-error"


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


def _search_data(route, departure_date):
    origin, destination, _airline = route
    return {
        "origin": origin.pk,
        "destination": destination.pk,
        "departure_date": departure_date.isoformat(),
    }


def test_flight_search_date_input_minimum_is_today(route):
    form = FlightSearchForm()

    assert form.fields["departure_date"].widget.attrs["min"] == timezone.localdate().isoformat()


@pytest.mark.parametrize("day_offset", [0, 1, 30])
def test_flight_search_accepts_today_and_future_dates(route, day_offset):
    form = FlightSearchForm(_search_data(route, timezone.localdate() + timedelta(days=day_offset)))

    assert form.is_valid()


def test_flight_search_rejects_yesterday(route):
    form = FlightSearchForm(_search_data(route, timezone.localdate() - timedelta(days=1)))

    assert not form.is_valid()
    assert form.errors["departure_date"] == ["Departure date cannot be in the past."]


@override_settings(USE_TZ=True, TIME_ZONE="Asia/Tokyo")
def test_flight_search_uses_configured_timezone_local_date(route):
    utc_instant = datetime(2026, 1, 1, 15, 30, tzinfo=UTC)
    with patch("django.utils.timezone.now", return_value=utc_instant):
        form = FlightSearchForm(_search_data(route, utc_instant.date()))

    assert form.fields["departure_date"].widget.attrs["min"] == "2026-01-02"
    assert not form.is_valid()
    assert form.errors["departure_date"] == ["Departure date cannot be in the past."]
