from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
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
SEAT_NUMBERS = ("1A", "1B", "2A", "2B", "3A", "3B")


class Command(BaseCommand):
    help = "Create or refresh non-destructive course demonstration data."

    @transaction.atomic
    def handle(self, *args, **options):
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
            flight, _ = Flight.objects.update_or_create(
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
            for seat_number in SEAT_NUMBERS:
                Seat.objects.get_or_create(flight=flight, seat_number=seat_number)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data ready: {len(cities)} cities, {len(airlines)} airlines, "
                f"{len(seeded_flights)} flights."
            )
        )
