from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from reservations.models import Flight, Seat

PENDING_BOOKING_SESSION_KEY = "pending_booking"
PENDING_BOOKING_VERSION = 1


@dataclass(frozen=True)
class PendingBooking:
    flight_id: int
    seat_id: int
    passenger_name: str
    passenger_email: str

    def as_form_data(self):
        return {
            "seat": str(self.seat_id),
            "passenger_name": self.passenger_name,
            "passenger_email": self.passenger_email,
        }


def store_pending_booking(request, *, flight, seat, passenger_name, passenger_email):
    request.session[PENDING_BOOKING_SESSION_KEY] = {
        "version": PENDING_BOOKING_VERSION,
        "flight_id": flight.pk,
        "seat_id": seat.pk,
        "passenger_name": passenger_name,
        "passenger_email": passenger_email,
    }


def clear_pending_booking(request):
    request.session.pop(PENDING_BOOKING_SESSION_KEY, None)


def load_pending_booking(request):
    value = request.session.get(PENDING_BOOKING_SESSION_KEY)
    if not isinstance(value, dict) or set(value) != {
        "version",
        "flight_id",
        "seat_id",
        "passenger_name",
        "passenger_email",
    }:
        clear_pending_booking(request)
        return None

    version = value.get("version")
    flight_id = value.get("flight_id")
    seat_id = value.get("seat_id")
    passenger_name = value.get("passenger_name")
    passenger_email = value.get("passenger_email")
    if (
        version != PENDING_BOOKING_VERSION
        or not isinstance(flight_id, int)
        or isinstance(flight_id, bool)
        or not isinstance(seat_id, int)
        or isinstance(seat_id, bool)
        or not isinstance(passenger_name, str)
        or not passenger_name.strip()
        or len(passenger_name) > 100
        or not isinstance(passenger_email, str)
    ):
        clear_pending_booking(request)
        return None

    passenger_name = passenger_name.strip()
    passenger_email = passenger_email.strip()
    try:
        validate_email(passenger_email)
    except ValidationError:
        clear_pending_booking(request)
        return None

    if (
        not Flight.objects.filter(pk=flight_id).exists()
        or not Seat.objects.filter(
            pk=seat_id,
            flight_id=flight_id,
        ).exists()
    ):
        clear_pending_booking(request)
        return None

    return PendingBooking(
        flight_id=flight_id,
        seat_id=seat_id,
        passenger_name=passenger_name,
        passenger_email=passenger_email,
    )
