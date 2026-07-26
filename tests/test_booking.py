from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone
from reservations.models import Airline, Booking, City, Flight, Seat
from reservations.pricing import calculate_booking_price
from reservations.services import SeatUnavailableError, create_guest_booking

pytestmark = pytest.mark.django_db


@pytest.fixture
def flight():
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    departure = timezone.now() + timedelta(days=1)
    return Flight.objects.create(
        airline=airline,
        flight_number="101",
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=1),
    )


@pytest.mark.parametrize(
    ("fare", "taxes", "total"),
    [
        ("15000", "1500", "16500"),
        ("15005", "1501", "16506"),
        ("0", "0", "0"),
    ],
)
def test_whole_yen_price_calculation(fare, taxes, total):
    price = calculate_booking_price(Decimal(fare))

    assert price.base_fare == Decimal(fare)
    assert price.taxes_and_fees == Decimal(taxes)
    assert price.total_price == Decimal(total)


def test_fractional_base_fare_rounds_half_up_to_whole_yen():
    price = calculate_booking_price(Decimal("100.5"))

    assert price.base_fare == Decimal("101")
    assert price.taxes_and_fees == Decimal("10")
    assert price.total_price == Decimal("111")


def test_booking_reference_is_unique_and_readable(flight):
    first = Booking.objects.create(
        seat=Seat.objects.create(flight=flight, seat_number="1A"),
        guest_name="First",
        guest_email="first@example.com",
    )
    second = Booking.objects.create(
        seat=Seat.objects.create(flight=flight, seat_number="1B"),
        guest_name="Second",
        guest_email="second@example.com",
    )

    assert first.booking_reference != second.booking_reference
    assert len(first.booking_reference) == 12
    assert first.booking_reference.startswith("SKY-")


def test_database_rejects_duplicate_booking_reference(flight):
    first = Booking.objects.create(
        seat=Seat.objects.create(flight=flight, seat_number="1A"),
        guest_name="First",
        guest_email="first@example.com",
        booking_reference="SKY-ABCDEFGH",
    )

    with pytest.raises(IntegrityError), transaction.atomic():
        Booking.objects.create(
            seat=Seat.objects.create(flight=flight, seat_number="1B"),
            guest_name="Second",
            guest_email="second@example.com",
            booking_reference=first.booking_reference,
        )


def test_service_retries_reference_collision(flight):
    Seat.objects.create(flight=flight, seat_number="1A")
    Booking.objects.create(
        seat=flight.seats.get(),
        guest_name="First",
        guest_email="first@example.com",
        booking_reference="SKY-ABCDEFGH",
    )
    target_seat = Seat.objects.create(flight=flight, seat_number="1B", price=Decimal("20000"))

    with patch(
        "reservations.services.generate_booking_reference",
        side_effect=["SKY-ABCDEFGH", "SKY-JKLMNPQR"],
    ):
        booking = create_guest_booking(
            flight=flight,
            seat=target_seat,
            passenger_name="Second",
            passenger_email="second@example.com",
        )

    assert booking.booking_reference == "SKY-JKLMNPQR"
    assert booking.total_price == Decimal("22000")


def test_service_rejects_booked_seat(flight):
    seat = Seat.objects.create(flight=flight, seat_number="1A")
    Booking.objects.create(
        seat=seat,
        guest_name="First",
        guest_email="first@example.com",
    )

    with pytest.raises(SeatUnavailableError):
        create_guest_booking(
            flight=flight,
            seat=seat,
            passenger_name="Second",
            passenger_email="second@example.com",
        )


def test_service_rejects_seat_from_another_flight(flight):
    other_destination = City.objects.create(name="Sapporo", code="SPK")
    other_flight = Flight.objects.create(
        airline=flight.airline,
        flight_number="202",
        origin=flight.origin,
        destination=other_destination,
        departure_time=flight.departure_time,
        arrival_time=flight.arrival_time,
    )
    other_seat = Seat.objects.create(flight=other_flight, seat_number="1A")

    with pytest.raises(
        SeatUnavailableError,
        match="The selected seat does not belong to this flight.",
    ):
        create_guest_booking(
            flight=flight,
            seat=other_seat,
            passenger_name="Guest",
            passenger_email="guest@example.com",
        )

    assert not Booking.objects.filter(seat=other_seat).exists()
