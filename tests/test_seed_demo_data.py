from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.urls import reverse
from django.utils import timezone
from reservations.management.commands import seed_demo_data
from reservations.models import Airline, Booking, City, Flight, Seat

REQUIRED_REGIONS = {
    "Hokkaido",
    "Tohoku",
    "Kanto",
    "Chubu",
    "Kansai",
    "Chugoku",
    "Shikoku",
    "Kyushu",
    "Okinawa",
}


@pytest.mark.django_db
def test_seed_demo_data_populates_an_empty_database():
    call_command("seed_demo_data")

    assert 30 <= City.objects.count() <= 40
    assert Airline.objects.count() >= 2
    assert Flight.objects.count() == len(seed_demo_data.FLIGHT_DATA)
    assert (
        Flight.objects.filter(departure_time__gt=timezone.now()).count() == Flight.objects.count()
    )
    assert all(flight.seats.exists() for flight in Flight.objects.all())


def test_seed_catalog_has_stable_unique_codes_clear_names_and_regional_coverage():
    codes = [code for code, _, _ in seed_demo_data.CITY_DATA]
    names = [name for _, name, _ in seed_demo_data.CITY_DATA]
    regions = {region for _, _, region in seed_demo_data.CITY_DATA}

    assert 30 <= len(codes) <= 40
    assert len(codes) == len(set(codes))
    assert all(len(code) == 3 and code.isascii() and code.isupper() for code in codes)
    assert all(name.strip() and name == name.strip() for name in names)
    assert regions >= REQUIRED_REGIONS
    assert {
        ("TYO", "Tokyo"),
        ("OSA", "Osaka"),
        ("SPK", "Sapporo"),
        ("FUK", "Fukuoka"),
    } <= {(code, name) for code, name, _ in seed_demo_data.CITY_DATA}


def test_seed_catalog_routes_are_unique_valid_and_cover_every_destination():
    city_regions = {code: region for code, _, region in seed_demo_data.CITY_DATA}
    identities = [(airline_code, number) for airline_code, number, *_ in seed_demo_data.FLIGHT_DATA]
    used_codes = set()

    assert len(identities) == len(set(identities))
    for _, _, origin_code, destination_code, day_offset, _, duration in seed_demo_data.FLIGHT_DATA:
        assert origin_code in city_regions
        assert destination_code in city_regions
        assert origin_code != destination_code
        assert day_offset >= 0
        assert duration > timedelta(0)
        used_codes.update((origin_code, destination_code))

    assert used_codes == set(city_regions)
    assert {city_regions[code] for code in used_codes} == REQUIRED_REGIONS


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

    htmx_response = client.get(
        reverse("reservations:flight_list"),
        {
            "origin": flight.origin_id,
            "destination": flight.destination_id,
            "departure_date": timezone.localtime(flight.departure_time).date().isoformat(),
        },
        headers={"HX-Request": "true"},
    )
    assert list(htmx_response.context["flights"]) == list(search_response.context["flights"])
    assert flight.flight_number in htmx_response.content.decode()
    assert "<!DOCTYPE html>" not in htmx_response.content.decode()


@pytest.mark.django_db
def test_seeded_available_seats_appear_in_booking_form(client):
    call_command("seed_demo_data")
    seat = Seat.objects.first()

    response = client.get(reverse("reservations:flight_booking", args=[seat.flight_id]))

    assert seat in response.context["form"].fields["seat"].queryset
    assert seat.seat_number in response.content.decode()


@pytest.mark.django_db
def test_seeded_seats_cover_cabins_types_and_varied_prices():
    call_command("seed_demo_data")

    assert set(Seat.objects.values_list("cabin_class", flat=True)) == {
        Seat.CabinClass.ECONOMY,
        Seat.CabinClass.BUSINESS,
    }
    assert set(Seat.objects.values_list("seat_type", flat=True)) == {
        Seat.SeatType.WINDOW,
        Seat.SeatType.MIDDLE,
        Seat.SeatType.AISLE,
    }
    assert Seat.objects.values("price").distinct().count() >= 6
    assert all(
        flight.seats.filter(cabin_class=Seat.CabinClass.ECONOMY).exists()
        and flight.seats.filter(cabin_class=Seat.CabinClass.BUSINESS).exists()
        and set(flight.seats.values_list("seat_type", flat=True))
        == {
            Seat.SeatType.WINDOW,
            Seat.SeatType.MIDDLE,
            Seat.SeatType.AISLE,
        }
        and not flight.seats.filter(price__lte=0).exists()
        for flight in Flight.objects.all()
    )


@pytest.mark.django_db
def test_seed_demo_data_preserves_existing_records_and_bookings():
    existing_catalog_city = City.objects.create(code="NGO", name="Persisted Nagoya")
    unrelated_city = City.objects.create(code="WKJ", name="Wakkanai")
    call_command("seed_demo_data")
    seat = Seat.objects.first()
    Booking.objects.create(
        seat=seat,
        guest_name="Existing Guest",
        guest_email="existing@example.com",
    )
    city_snapshot = list(City.objects.order_by("pk").values())
    flight_snapshot = list(Flight.objects.order_by("pk").values())
    seat_snapshot = list(Seat.objects.order_by("pk").values())
    booking_snapshot = list(Booking.objects.order_by("pk").values())
    counts_before = {
        "cities": City.objects.count(),
        "airlines": Airline.objects.count(),
        "flights": Flight.objects.count(),
        "seats": Seat.objects.count(),
        "bookings": Booking.objects.count(),
    }

    call_command("seed_demo_data")

    assert City.objects.get(pk=existing_catalog_city.pk).name == "Persisted Nagoya"
    assert City.objects.get(pk=unrelated_city.pk).name == "Wakkanai"
    assert list(City.objects.order_by("pk").values()) == city_snapshot
    assert list(Flight.objects.order_by("pk").values()) == flight_snapshot
    assert list(Seat.objects.order_by("pk").values()) == seat_snapshot
    assert list(Booking.objects.order_by("pk").values()) == booking_snapshot
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
    Booking.objects.create(
        seat=seat,
        guest_name="Existing Guest",
        guest_email="existing@example.com",
    )
    departure_time = flight.departure_time
    arrival_time = flight.arrival_time
    origin_id = flight.origin_id
    destination_id = flight.destination_id
    seat_snapshot = list(flight.seats.order_by("pk").values())
    booking_snapshot = list(Booking.objects.order_by("pk").values())
    flight_count = Flight.objects.count()
    seat_count = Seat.objects.count()

    with patch.object(seed_demo_data.timezone, "localdate", return_value=date(2026, 8, 2)):
        call_command("seed_demo_data")

    flight.refresh_from_db()
    assert flight.departure_time == departure_time
    assert flight.arrival_time == arrival_time
    assert flight.origin_id == origin_id
    assert flight.destination_id == destination_id
    assert list(flight.seats.order_by("pk").values()) == seat_snapshot
    assert list(Booking.objects.order_by("pk").values()) == booking_snapshot
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


@pytest.mark.django_db
def test_seed_demo_data_rejects_duplicate_destination_codes_before_writing(monkeypatch):
    duplicate = ("TYO", "Other Tokyo", "Kanto")
    monkeypatch.setattr(seed_demo_data, "CITY_DATA", (*seed_demo_data.CITY_DATA, duplicate))

    with pytest.raises(CommandError, match="destination codes must be unique"):
        call_command("seed_demo_data")

    assert City.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_flight",
    [
        ("SKY", "D998", "XXX", "TYO", 1, seed_demo_data.time(9, 0), timedelta(hours=1)),
        ("SKY", "D997", "TYO", "OSA", 1, seed_demo_data.time(9, 0), timedelta(0)),
    ],
)
def test_seed_demo_data_rejects_unknown_endpoints_and_non_positive_schedules(
    monkeypatch, invalid_flight
):
    monkeypatch.setattr(
        seed_demo_data, "FLIGHT_DATA", (*seed_demo_data.FLIGHT_DATA, invalid_flight)
    )

    with pytest.raises(CommandError):
        call_command("seed_demo_data")

    assert City.objects.count() == 0


@pytest.mark.django_db
def test_seed_demo_data_does_not_mutate_an_existing_seeded_seat():
    call_command("seed_demo_data")
    seat = Seat.objects.first()
    seat.cabin_class = Seat.CabinClass.ECONOMY
    seat.seat_type = Seat.SeatType.AISLE
    seat.price = Decimal("12345")
    seat.save()

    call_command("seed_demo_data")

    seat.refresh_from_db()
    assert seat.cabin_class == Seat.CabinClass.ECONOMY
    assert seat.seat_type == Seat.SeatType.AISLE
    assert seat.price == Decimal("12345")
