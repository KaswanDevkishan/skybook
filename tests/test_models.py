from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from reservations.models import Airline, Booking, City, Flight, Seat

pytestmark = pytest.mark.django_db


def make_route():
    origin = City.objects.create(name="Tokyo", code=" hnd ")
    destination = City.objects.create(name="Sapporo", code="cts")
    airline = Airline.objects.create(name="SkyBook Air", code=" sb ")
    return origin, destination, airline


def make_flight(*, departure_offset=timedelta(), flight_number="101"):
    origin, destination, airline = make_route()
    departure = timezone.now() + timedelta(days=1) + departure_offset
    return Flight.objects.create(
        airline=airline,
        flight_number=flight_number,
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=2),
    )


def assert_integrity_error(create_record):
    with pytest.raises(IntegrityError), transaction.atomic():
        create_record()


def test_city_normalizes_code_and_has_useful_string():
    city = City.objects.create(name="Tokyo", code=" hnd ")

    assert city.code == "HND"
    assert str(city) == "Tokyo (HND)"


def test_city_code_is_unique_after_normalization():
    City.objects.create(name="Tokyo", code="hnd")

    assert_integrity_error(lambda: City.objects.create(name="Other", code=" HND "))


def test_airline_normalizes_code_and_has_useful_string():
    airline = Airline.objects.create(name="SkyBook Air", code=" sb ")

    assert airline.code == "SB"
    assert str(airline) == "SkyBook Air (SB)"


def test_airline_code_is_unique_after_normalization():
    Airline.objects.create(name="SkyBook Air", code="sb")

    assert_integrity_error(lambda: Airline.objects.create(name="Other", code=" SB "))


def test_valid_flight_relationships_and_string():
    flight = make_flight()

    assert flight.origin.code == "HND"
    assert flight.destination.code == "CTS"
    assert flight.airline.code == "SB"
    assert str(flight) == "SB101: HND → CTS"


def test_flight_rejects_same_origin_and_destination():
    city = City.objects.create(name="Tokyo", code="HND")
    airline = Airline.objects.create(name="SkyBook Air", code="SB")
    departure = timezone.now() + timedelta(days=1)

    assert_integrity_error(
        lambda: Flight.objects.create(
            airline=airline,
            flight_number="101",
            origin=city,
            destination=city,
            departure_time=departure,
            arrival_time=departure + timedelta(hours=2),
        )
    )


@pytest.mark.parametrize("arrival_delta", [timedelta(), timedelta(minutes=-1)])
def test_flight_rejects_arrival_not_after_departure(arrival_delta):
    origin, destination, airline = make_route()
    departure = timezone.now() + timedelta(days=1)

    assert_integrity_error(
        lambda: Flight.objects.create(
            airline=airline,
            flight_number="101",
            origin=origin,
            destination=destination,
            departure_time=departure,
            arrival_time=departure + arrival_delta,
        )
    )


def test_flight_rejects_duplicate_scheduled_identity():
    flight = make_flight()

    assert_integrity_error(
        lambda: Flight.objects.create(
            airline=flight.airline,
            flight_number=flight.flight_number,
            origin=flight.origin,
            destination=flight.destination,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time,
        )
    )


def test_seat_number_is_unique_per_flight_and_string_identifies_flight():
    first_flight = make_flight()
    second_flight = Flight.objects.create(
        airline=first_flight.airline,
        flight_number=first_flight.flight_number,
        origin=first_flight.origin,
        destination=first_flight.destination,
        departure_time=first_flight.departure_time + timedelta(days=1),
        arrival_time=first_flight.arrival_time + timedelta(days=1),
    )

    first_seat = Seat.objects.create(flight=first_flight, seat_number=" 12a ")
    second_seat = Seat.objects.create(flight=second_flight, seat_number="12A")

    assert first_seat.seat_number == "12A"
    assert second_seat.seat_number == "12A"
    assert str(first_seat) == "SB101: HND → CTS — seat 12A"
    assert_integrity_error(lambda: Seat.objects.create(flight=first_flight, seat_number="12a"))


def test_seat_choices_and_whole_yen_price_are_persisted():
    seat = Seat.objects.create(
        flight=make_flight(),
        seat_number="1A",
        cabin_class=Seat.CabinClass.BUSINESS,
        seat_type=Seat.SeatType.WINDOW,
        price=Decimal("52000"),
    )

    assert Seat.CabinClass.values == ["ECONOMY", "BUSINESS"]
    assert Seat.SeatType.values == ["WINDOW", "MIDDLE", "AISLE"]
    assert seat.get_cabin_class_display() == "Business"
    assert seat.get_seat_type_display() == "Window"
    assert seat.price == Decimal("52000")


def test_seat_rejects_negative_price_during_validation():
    seat = Seat(flight=make_flight(), seat_number="1A", price=Decimal("-1"))

    with pytest.raises(ValidationError):
        seat.full_clean()


def test_registered_user_booking_and_string():
    user = get_user_model().objects.create_user(username="traveler", password="secret-pass")
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")

    booking = Booking.objects.create(seat=seat, user=user)

    assert booking.user == user
    assert str(booking) == (
        f"{booking.booking_reference}: SB101: HND → CTS — seat 1A booked for traveler"
    )


def test_guest_booking_and_string():
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")

    booking = Booking(
        seat=seat,
        guest_name="Guest Traveler",
        guest_email="guest@example.com",
    )
    booking.full_clean()
    booking.save()

    assert booking.user is None
    assert str(booking) == (
        f"{booking.booking_reference}: SB101: HND → CTS — seat 1A booked for Guest Traveler"
    )
    assert booking.booking_reference.startswith("SKY-")
    assert booking.base_fare == Decimal("15000")
    assert booking.taxes_and_fees == Decimal("1500")
    assert booking.total_price == Decimal("16500")
    assert booking.created_at is not None


def test_database_rejects_booking_without_user_or_guest_details():
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")

    assert_integrity_error(lambda: Booking.objects.create(seat=seat))


@pytest.mark.parametrize(
    ("guest_name", "guest_email"),
    [
        ("Guest Traveler", ""),
        ("", "guest@example.com"),
        ("   ", "guest@example.com"),
        ("Guest Traveler", "   "),
    ],
)
def test_database_rejects_incomplete_guest_details(guest_name, guest_email):
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")

    assert_integrity_error(
        lambda: Booking.objects.create(
            seat=seat,
            guest_name=guest_name,
            guest_email=guest_email,
        )
    )


def test_guest_booking_requires_name_and_email_during_model_validation():
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")
    booking = Booking(seat=seat, guest_name="", guest_email="")

    with pytest.raises(ValidationError, match="Guest bookings require"):
        booking.full_clean()


def test_booking_survives_registered_user_deletion():
    user = get_user_model().objects.create_user(username="traveler")
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")
    booking = Booking.objects.create(
        seat=seat,
        user=user,
        guest_name="Traveler",
        guest_email="traveler@example.com",
    )

    user.delete()
    booking.refresh_from_db()

    assert booking.user is None


def test_referenced_airline_and_cities_are_protected_from_deletion():
    flight = make_flight()

    for referenced_object in (flight.airline, flight.origin, flight.destination):
        with pytest.raises(ProtectedError):
            referenced_object.delete()


def test_booked_seat_is_protected_from_deletion():
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")
    Booking.objects.create(
        seat=seat,
        guest_name="Guest Traveler",
        guest_email="guest@example.com",
    )

    with pytest.raises(ProtectedError):
        seat.delete()


def test_database_rejects_second_booking_for_same_seat():
    seat = Seat.objects.create(flight=make_flight(), seat_number="1A")
    Booking.objects.create(
        seat=seat,
        guest_name="First Guest",
        guest_email="first@example.com",
    )

    assert_integrity_error(
        lambda: Booking.objects.create(
            seat=seat,
            guest_name="Second Guest",
            guest_email="second@example.com",
        )
    )


def test_all_domain_models_are_registered_in_admin():
    for model in (City, Airline, Flight, Seat, Booking):
        assert admin.site.is_registered(model)
