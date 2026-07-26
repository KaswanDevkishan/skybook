from django.db.models import Count, Exists, IntegerField, Min, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from reservations.models import Booking, Flight, Seat


def flights_with_availability(queryset=None):
    queryset = queryset if queryset is not None else Flight.objects.all()
    available_seats = Seat.objects.filter(flight=OuterRef("pk")).exclude(
        bookings__status=Booking.Status.CONFIRMED
    )
    available_seat_count = (
        available_seats.order_by()
        .values("flight")
        .annotate(total=Count("pk", distinct=True))
        .values("total")
    )
    lowest_available_price = (
        available_seats.order_by().values("flight").annotate(price=Min("price")).values("price")
    )
    return (
        queryset.select_related("airline", "origin", "destination")
        .annotate(
            available_seat_count=Coalesce(
                Subquery(available_seat_count, output_field=IntegerField()),
                Value(0),
            ),
            lowest_available_price=Subquery(lowest_available_price),
            economy_available=Exists(available_seats.filter(cabin_class=Seat.CabinClass.ECONOMY)),
            business_available=Exists(available_seats.filter(cabin_class=Seat.CabinClass.BUSINESS)),
        )
        .order_by("departure_time")
    )
