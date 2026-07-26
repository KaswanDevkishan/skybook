from datetime import date, timedelta
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.urls import reverse
from django.utils import timezone
from reservations.management.commands import seed_demo_data
from reservations.models import Airline, Booking, City, Flight, Seat


@pytest.mark.django_db
def test_seed_demo_data_populates_an_empty_database():
    call_command("seed_demo_data")

    assert City.objects.count() >= 4
    assert Airline.objects.count() >= 2
    assert Flight.objects.count() >= 4
    assert (
        Flight.objects.filter(departure_time__gt=timezone.now()).count() == Flight.objects.count()
    )
    assert all(flight.seats.exists() for flight in Flight.objects.all())


@pytest.mark.django_db
def test_seed_demo_data_is_idempotent():
    call_command("seed_demo_data")
    first_counts = (
        City.objects.count(),
        Airline.objects.count(),
        Flight.objects.count(),
        Seat.objects.count(),
    )

    call_command("seed_demo_data")

    assert (
        City.objects.count(),
        Airline.objects.count(),
        Flight.objects.count(),
        Seat.objects.count(),
    ) == first_counts


@pytest.mark.django_db
def test_seeded_cities_and_flights_appear_in_flight_search(client):
    call_command("seed_demo_data")
    flight = Flight.objects.order_by("departure_time").first()

    form_response = client.get(reverse("reservations:flight_list"))
    assert flight.origin in form_response.context["form"].fields["origin"].queryset
    assert flight.destination in form_response.context["form"].fields["destination"].queryset

    search_response = client.get(
        reverse("reservations:flight_list"),
        {
            "origin": flight.origin_id,
            "destination": flight.destination_id,
            "departure_date": timezone.localtime(flight.departure_time).date().isoformat(),
        },
    )

    assert flight in search_response.context["flights"]
    assert flight.flight_number in search_response.content.decode()


@pytest.mark.django_db
def test_seeded_available_seats_appear_in_booking_form(client):
    call_command("seed_demo_data")
    seat = Seat.objects.first()

    response = client.get(reverse("reservations:booking_new"))

    assert seat in response.context["form"].fields["seat"].queryset
    assert str(seat) in response.content.decode()


@pytest.mark.django_db
def test_seed_demo_data_preserves_existing_records_and_bookings():
    unrelated_city = City.objects.create(code="NGO", name="Nagoya")
    call_command("seed_demo_data")
    seat = Seat.objects.first()
    booking = Booking.objects.create(
        seat=seat,
        guest_name="Existing Guest",
        guest_email="existing@example.com",
    )
    counts_before = {
        "cities": City.objects.count(),
        "airlines": Airline.objects.count(),
        "flights": Flight.objects.count(),
        "seats": Seat.objects.count(),
        "bookings": Booking.objects.count(),
    }

    call_command("seed_demo_data")

    assert City.objects.get(pk=unrelated_city.pk).name == "Nagoya"
    assert Booking.objects.get(pk=booking.pk).seat_id == seat.pk
    assert {
        "cities": City.objects.count(),
        "airlines": Airline.objects.count(),
        "flights": Flight.objects.count(),
        "seats": Seat.objects.count(),
        "bookings": Booking.objects.count(),
    } == counts_before
    assert Flight.objects.filter(
        departure_time__date__gte=timezone.localdate() + timedelta(days=1)
    ).exists()


@pytest.mark.django_db
def test_seed_demo_data_preserves_booked_flight_schedule_when_deployment_date_advances():
    with patch.object(seed_demo_data.timezone, "localdate", return_value=date(2026, 7, 26)):
        call_command("seed_demo_data")

    flight = Flight.objects.get(airline__code="SKY", flight_number="D101")
    seat = flight.seats.get(seat_number="1A")
    booking = Booking.objects.create(
        seat=seat,
        guest_name="Existing Guest",
        guest_email="existing@example.com",
    )
    departure_time = flight.departure_time
    arrival_time = flight.arrival_time
    flight_count = Flight.objects.count()
    seat_count = Seat.objects.count()

    with patch.object(seed_demo_data.timezone, "localdate", return_value=date(2026, 8, 2)):
        call_command("seed_demo_data")

    flight.refresh_from_db()
    assert flight.departure_time == departure_time
    assert flight.arrival_time == arrival_time
    assert Booking.objects.get(pk=booking.pk).seat_id == seat.pk
    assert Seat.objects.filter(pk=seat.pk, flight=flight).exists()
    assert Flight.objects.count() == flight_count
    assert Seat.objects.count() == seat_count


@pytest.mark.django_db
def test_seed_demo_data_rejects_a_route_with_the_same_origin_and_destination(monkeypatch):
    invalid_flight = ("SKY", "D999", "TYO", "TYO", 1, seed_demo_data.time(9, 0), timedelta(hours=1))
    monkeypatch.setattr(
        seed_demo_data, "FLIGHT_DATA", (*seed_demo_data.FLIGHT_DATA, invalid_flight)
    )

    with pytest.raises(CommandError, match="D999 must have different origin and destination"):
        call_command("seed_demo_data")

    assert Flight.objects.count() == 0
