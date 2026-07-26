from datetime import timedelta
from decimal import Decimal

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.utils import timezone

pytestmark = pytest.mark.django_db(transaction=True)


def test_pricing_migration_preserves_and_backfills_existing_booking():
    executor = MigrationExecutor(connection)
    executor.migrate([("reservations", "0002_booking_booking_has_user_or_guest_details")])
    old_apps = executor.loader.project_state(
        [("reservations", "0002_booking_booking_has_user_or_guest_details")]
    ).apps

    City = old_apps.get_model("reservations", "City")
    Airline = old_apps.get_model("reservations", "Airline")
    Flight = old_apps.get_model("reservations", "Flight")
    Seat = old_apps.get_model("reservations", "Seat")
    Booking = old_apps.get_model("reservations", "Booking")
    User = old_apps.get_model("auth", "User")

    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")
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
    seat = Seat.objects.create(flight=flight, seat_number="1A")
    booking = Booking.objects.create(
        seat=seat,
        guest_name="Existing Guest",
        guest_email="existing@example.com",
    )
    registered_seat = Seat.objects.create(flight=flight, seat_number="1B")
    user = User.objects.create(username="registered")
    registered_booking = Booking.objects.create(seat=registered_seat, user=user)

    executor = MigrationExecutor(connection)
    executor.migrate([("reservations", "0003_booking_prices_and_seat_classification")])
    new_apps = executor.loader.project_state(
        [("reservations", "0003_booking_prices_and_seat_classification")]
    ).apps
    MigratedSeat = new_apps.get_model("reservations", "Seat")
    MigratedBooking = new_apps.get_model("reservations", "Booking")

    migrated_seat = MigratedSeat.objects.get(pk=seat.pk)
    migrated_booking = MigratedBooking.objects.get(pk=booking.pk)
    migrated_registered_booking = MigratedBooking.objects.get(pk=registered_booking.pk)

    assert migrated_seat.flight_id == flight.pk
    assert migrated_seat.cabin_class == "ECONOMY"
    assert migrated_seat.seat_type == "WINDOW"
    assert migrated_seat.price == Decimal("15000")
    assert migrated_booking.seat_id == seat.pk
    assert migrated_booking.base_fare == Decimal("15000")
    assert migrated_booking.taxes_and_fees == Decimal("1500")
    assert migrated_booking.total_price == Decimal("16500")
    assert migrated_booking.booking_reference.startswith("SKY-")
    assert migrated_registered_booking.user_id == user.pk
    assert migrated_registered_booking.seat_id == registered_seat.pk
    assert migrated_registered_booking.booking_reference != migrated_booking.booking_reference


def test_status_migration_defaults_existing_bookings_to_confirmed():
    executor = MigrationExecutor(connection)
    executor.migrate([("reservations", "0003_booking_prices_and_seat_classification")])
    old_apps = executor.loader.project_state(
        [("reservations", "0003_booking_prices_and_seat_classification")]
    ).apps

    City = old_apps.get_model("reservations", "City")
    Airline = old_apps.get_model("reservations", "Airline")
    Flight = old_apps.get_model("reservations", "Flight")
    Seat = old_apps.get_model("reservations", "Seat")
    Booking = old_apps.get_model("reservations", "Booking")
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Osaka", code="OSA")
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
    booking = Booking.objects.create(
        seat=Seat.objects.create(flight=flight, seat_number="1A"),
        guest_name="Historical Guest",
        guest_email="historical@example.com",
        booking_reference="SKY-HISTORY1",
        base_fare=Decimal("12345"),
        taxes_and_fees=Decimal("1235"),
        total_price=Decimal("13580"),
    )

    executor = MigrationExecutor(connection)
    executor.migrate([("reservations", "0004_booking_status")])
    new_apps = executor.loader.project_state([("reservations", "0004_booking_status")]).apps
    MigratedBooking = new_apps.get_model("reservations", "Booking")
    migrated = MigratedBooking.objects.get(pk=booking.pk)

    assert migrated.status == "CONFIRMED"
    assert migrated.booking_reference == "SKY-HISTORY1"
    assert migrated.guest_name == "Historical Guest"
    assert migrated.guest_email == "historical@example.com"
    assert migrated.base_fare == Decimal("12345")
    assert migrated.taxes_and_fees == Decimal("1235")
    assert migrated.total_price == Decimal("13580")
