from django.db.models import Count, Exists, Min, OuterRef, Q

from reservations.models import Flight, Seat


def flights_with_availability(queryset=None):
    queryset = queryset if queryset is not None else Flight.objects.all()
    available_seats = Seat.objects.filter(flight=OuterRef("pk"), bookings__isnull=True)
    return (
        queryset.select_related("airline", "origin", "destination")
        .annotate(
            available_seat_count=Count(
                "seats",
                filter=Q(seats__bookings__isnull=True),
                distinct=True,
            ),
            lowest_available_price=Min(
                "seats__price",
                filter=Q(seats__bookings__isnull=True),
            ),
            economy_available=Exists(available_seats.filter(cabin_class=Seat.CabinClass.ECONOMY)),
            business_available=Exists(available_seats.filter(cabin_class=Seat.CabinClass.BUSINESS)),
        )
        .order_by("departure_time")
    )
