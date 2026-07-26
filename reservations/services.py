from django.db import IntegrityError, transaction

from reservations.models import Booking, Seat, generate_booking_reference
from reservations.pricing import calculate_booking_price

REFERENCE_ATTEMPTS = 10


class SeatUnavailableError(Exception):
    pass


class BookingReferenceError(Exception):
    pass


def create_guest_booking(*, flight, seat, passenger_name, passenger_email):
    for _ in range(REFERENCE_ATTEMPTS):
        try:
            with transaction.atomic():
                locked_seat = Seat.objects.select_for_update().get(pk=seat.pk)
                if locked_seat.flight_id != flight.pk:
                    raise ValueError("The selected seat does not belong to this flight.")
                if Booking.objects.filter(seat=locked_seat).exists():
                    raise SeatUnavailableError("This seat is already booked.")

                reference = generate_booking_reference()
                if Booking.objects.filter(booking_reference=reference).exists():
                    continue

                price = calculate_booking_price(locked_seat.price)
                return Booking.objects.create(
                    seat=locked_seat,
                    guest_name=passenger_name,
                    guest_email=passenger_email,
                    base_fare=price.base_fare,
                    taxes_and_fees=price.taxes_and_fees,
                    total_price=price.total_price,
                    booking_reference=reference,
                )
        except IntegrityError:
            if Booking.objects.filter(seat_id=seat.pk).exists():
                raise SeatUnavailableError("This seat was booked before confirmation.") from None

    raise BookingReferenceError("A unique booking reference could not be generated.")
