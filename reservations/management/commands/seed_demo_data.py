from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from reservations.models import Airline, City, Flight, Seat

CITY_DATA = (
    ("TYO", "Tokyo"),
    ("OSA", "Osaka"),
    ("SPK", "Sapporo"),
    ("FUK", "Fukuoka"),
)
AIRLINE_DATA = (
    ("SKY", "SkyBook Air"),
    ("WEB", "Web Wings"),
)
FLIGHT_DATA = (
    ("SKY", "D101", "TYO", "OSA", 1, time(9, 0), timedelta(hours=1, minutes=15)),
    ("SKY", "D102", "OSA", "FUK", 2, time(11, 30), timedelta(hours=1, minutes=20)),
    ("WEB", "D201", "TYO", "SPK", 3, time(8, 15), timedelta(hours=1, minutes=35)),
    ("WEB", "D202", "FUK", "TYO", 4, time(14, 0), timedelta(hours=1, minutes=45)),
    ("SKY", "D103", "SPK", "OSA", 6, time(10, 45), timedelta(hours=2)),
)
SEAT_DATA = (
    ("1A", Seat.CabinClass.BUSINESS, Seat.SeatType.WINDOW, 52000),
    ("1B", Seat.CabinClass.BUSINESS, Seat.SeatType.MIDDLE, 48000),
    ("1C", Seat.CabinClass.BUSINESS, Seat.SeatType.AISLE, 50000),
    ("2A", Seat.CabinClass.ECONOMY, Seat.SeatType.WINDOW, 18000),
    ("2B", Seat.CabinClass.ECONOMY, Seat.SeatType.MIDDLE, 15000),
    ("2C", Seat.CabinClass.ECONOMY, Seat.SeatType.AISLE, 16500),
    ("3A", Seat.CabinClass.ECONOMY, Seat.SeatType.WINDOW, 16000),
    ("3B", Seat.CabinClass.ECONOMY, Seat.SeatType.MIDDLE, 13500),
    ("3C", Seat.CabinClass.ECONOMY, Seat.SeatType.AISLE, 14500),
)


class Command(BaseCommand):
    help = "Create missing non-destructive course demonstration data."

    @transaction.atomic
    def handle(self, *args, **options):
        for _, flight_number, origin_code, destination_code, *_ in FLIGHT_DATA:
            if origin_code == destination_code:
                raise CommandError(
                    f"Seeded flight {flight_number} must have different origin and "
                    "destination codes."
                )

        cities = {
            code: City.objects.get_or_create(code=code, defaults={"name": name})[0]
            for code, name in CITY_DATA
        }
        airlines = {
            code: Airline.objects.get_or_create(code=code, defaults={"name": name})[0]
            for code, name in AIRLINE_DATA
        }

        schedule_start = timezone.localdate() + timedelta(days=1)
        seeded_flights = []
        for (
            airline_code,
            flight_number,
            origin_code,
            destination_code,
            day_offset,
            departure_clock,
            duration,
        ) in FLIGHT_DATA:
            departure_time = timezone.make_aware(
                datetime.combine(schedule_start + timedelta(days=day_offset), departure_clock)
            )
            flight, _ = Flight.objects.get_or_create(
                airline=airlines[airline_code],
                flight_number=flight_number,
                defaults={
                    "origin": cities[origin_code],
                    "destination": cities[destination_code],
                    "departure_time": departure_time,
                    "arrival_time": departure_time + duration,
                },
            )
            seeded_flights.append(flight)

        for flight in seeded_flights:
            for seat_number, cabin_class, seat_type, price in SEAT_DATA:
                Seat.objects.update_or_create(
                    flight=flight,
                    seat_number=seat_number,
                    defaults={
                        "cabin_class": cabin_class,
                        "seat_type": seat_type,
                        "price": price,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data ready: {len(cities)} cities, {len(airlines)} airlines, "
                f"{len(seeded_flights)} flights."
            )
        )
