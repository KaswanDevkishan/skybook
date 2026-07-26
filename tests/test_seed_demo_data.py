from datetime import timedelta

import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
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
