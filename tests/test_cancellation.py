from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from reservations.forms import BookingForm
from reservations.models import Airline, Booking, City, Flight, Seat
from reservations.queries import flights_with_availability
from reservations.services import create_booking

pytestmark = pytest.mark.django_db

PASSWORD = "SkyBook!4729Unique"


@pytest.fixture
def cancellation_data():
    owner = get_user_model().objects.create_user(username="owner", password=PASSWORD)
    other = get_user_model().objects.create_user(username="other", password=PASSWORD)
    origin = City.objects.create(name="Tokyo", code="TYO")
    destination = City.objects.create(name="Sapporo", code="SPK")
    airline = Airline.objects.create(name="SkyBook Air", code="SKY")
    departure = timezone.now() + timedelta(days=2)
    flight = Flight.objects.create(
        airline=airline,
        flight_number="401",
        origin=origin,
        destination=destination,
        departure_time=departure,
        arrival_time=departure + timedelta(hours=2),
    )
    seat = Seat.objects.create(
        flight=flight,
        seat_number="1A",
        price=Decimal("20000"),
    )
    booking = Booking.objects.create(
        seat=seat,
        user=owner,
        guest_name="Owner Passenger",
        guest_email="owner@example.com",
    )
    return owner, other, flight, seat, booking


def cancellation_url(booking):
    return reverse("reservations:cancel_booking", args=[booking.booking_reference])


def test_owner_can_view_confirmation_and_get_does_not_cancel(client, cancellation_data):
    owner, _, flight, seat, booking = cancellation_data
    client.force_login(owner)

    response = client.get(cancellation_url(booking))
    booking.refresh_from_db()
    content = response.content.decode()

    assert response.status_code == 200
    assert booking.status == Booking.Status.CONFIRMED
    assert booking.booking_reference in content
    assert f"{flight.airline.code}{flight.flight_number}" in content
    assert flight.origin.code in content
    assert flight.destination.code in content
    assert booking.guest_name in content
    assert seat.seat_number in content
    assert "¥22,000" in content
    assert "This action cancels your reservation" in content
    assert "no real refund" in content
    assert 'name="csrfmiddlewaretoken"' in content


def test_owner_can_cancel_via_post_without_losing_history_or_snapshots(client, cancellation_data):
    owner, _, _, _, booking = cancellation_data
    original = {
        "reference": booking.booking_reference,
        "name": booking.guest_name,
        "email": booking.guest_email,
        "base": booking.base_fare,
        "fees": booking.taxes_and_fees,
        "total": booking.total_price,
        "seat_id": booking.seat_id,
    }
    client.force_login(owner)

    response = client.post(cancellation_url(booking), follow=True)
    booking.refresh_from_db()

    assert response.redirect_chain[-1][0] == reverse("reservations:account")
    assert booking.status == Booking.Status.CANCELLED
    assert Booking.objects.filter(pk=booking.pk).exists()
    assert {
        "reference": booking.booking_reference,
        "name": booking.guest_name,
        "email": booking.guest_email,
        "base": booking.base_fare,
        "fees": booking.taxes_and_fees,
        "total": booking.total_price,
        "seat_id": booking.seat_id,
    } == original
    content = response.content.decode()
    receipt_url = reverse(
        "reservations:booking_confirmation",
        args=[booking.booking_reference],
    )
    assert "was cancelled" in content
    assert list(response.context["bookings"]) == []
    assert f'href="{receipt_url}"' not in content
    assert "You have no active bookings." in content
    assert "Find a flight" in content
    assert "Cancel booking" not in content


def test_cancelled_receipt_remains_owner_only(client, cancellation_data):
    owner, other, _, _, booking = cancellation_data
    receipt_url = reverse(
        "reservations:booking_confirmation",
        args=[booking.booking_reference],
    )
    client.force_login(owner)
    client.post(cancellation_url(booking))

    assert client.get(receipt_url).status_code == 200

    client.force_login(other)
    assert client.get(receipt_url).status_code == 404

    client.logout()
    assert client.get(receipt_url).status_code == 404


def test_cancellation_is_login_required_and_owner_scoped(client, cancellation_data):
    owner, other, _, _, booking = cancellation_data
    url = cancellation_url(booking)

    anonymous = client.get(url)
    assert anonymous.status_code == 302
    assert reverse("reservations:sign_in") in anonymous.url

    client.force_login(other)
    assert client.get(url).status_code == 404
    assert client.post(url).status_code == 404

    client.force_login(owner)
    guest = Booking.objects.create(
        seat=Seat.objects.create(flight=booking.seat.flight, seat_number="1B"),
        guest_name="Historical Guest",
        guest_email="guest@example.com",
    )
    assert client.get(cancellation_url(guest)).status_code == 404
    assert client.post(cancellation_url(guest)).status_code == 404
    guest.refresh_from_db()
    assert guest.status == Booking.Status.CONFIRMED


def test_cancellation_post_is_csrf_protected(cancellation_data):
    owner, _, _, _, booking = cancellation_data
    client = Client(enforce_csrf_checks=True)
    client.force_login(owner)

    assert client.post(cancellation_url(booking)).status_code == 403
    booking.refresh_from_db()
    assert booking.status == Booking.Status.CONFIRMED


def test_cancelled_seat_is_available_counted_and_can_be_rebooked(client, cancellation_data):
    owner, _, flight, seat, booking = cancellation_data
    client.force_login(owner)
    client.post(cancellation_url(booking))

    result = flights_with_availability().get(pk=flight.pk)
    form = BookingForm(flight=flight)
    detail = client.get(reverse("reservations:flight_booking", args=[flight.pk]))

    assert result.available_seat_count == 1
    assert result.lowest_available_price == seat.price
    assert list(form.fields["seat"].queryset) == [seat]
    assert "Available" in detail.content.decode()

    replacement = create_booking(
        flight=flight,
        seat=seat,
        passenger_name="Replacement Passenger",
        passenger_email="replacement@example.com",
    )
    booking.refresh_from_db()
    assert booking.status == Booking.Status.CANCELLED
    assert replacement.status == Booking.Status.CONFIRMED
    assert replacement.seat == seat

    with pytest.raises(IntegrityError), transaction.atomic():
        Booking.objects.create(
            seat=seat,
            guest_name="Duplicate",
            guest_email="duplicate@example.com",
        )


def test_past_booking_cannot_be_cancelled(client, cancellation_data):
    owner, _, flight, _, booking = cancellation_data
    flight.departure_time = timezone.now() - timedelta(minutes=1)
    flight.arrival_time = timezone.now() + timedelta(hours=1)
    flight.save(update_fields=["departure_time", "arrival_time"])
    client.force_login(owner)

    confirmation = client.get(cancellation_url(booking))
    response = client.post(cancellation_url(booking), follow=True)
    booking.refresh_from_db()

    assert "cannot be cancelled because the flight has departed" in confirmation.content.decode()
    assert "cannot be cancelled because the flight has departed" in response.content.decode()
    assert booking.status == Booking.Status.CONFIRMED
    assert "Cancel booking" not in client.get(reverse("reservations:account")).content.decode()


def test_repeated_cancellation_is_safe(client, cancellation_data):
    owner, _, _, _, booking = cancellation_data
    client.force_login(owner)

    first = client.post(cancellation_url(booking))
    second = client.post(cancellation_url(booking), follow=True)
    booking.refresh_from_db()

    assert first.status_code == 302
    assert second.status_code == 200
    assert booking.status == Booking.Status.CANCELLED
    assert Booking.objects.filter(pk=booking.pk).count() == 1
    assert "already cancelled" in second.content.decode()
