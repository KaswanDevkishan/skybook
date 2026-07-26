from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from reservations.models import Airline, City, Flight, Seat

CITY_DATA = (
    ("TYO", "Tokyo", "Kanto"),
    ("OSA", "Osaka", "Kansai"),
    ("SPK", "Sapporo", "Hokkaido"),
    ("FUK", "Fukuoka", "Kyushu"),
    ("CTS", "New Chitose", "Hokkaido"),
    ("HKD", "Hakodate", "Hokkaido"),
    ("AKJ", "Asahikawa", "Hokkaido"),
    ("AOJ", "Aomori", "Tohoku"),
    ("SDJ", "Sendai", "Tohoku"),
    ("AXT", "Akita", "Tohoku"),
    ("GAJ", "Yamagata", "Tohoku"),
    ("HND", "Tokyo Haneda", "Kanto"),
    ("NRT", "Tokyo Narita", "Kanto"),
    ("NGO", "Nagoya Chubu Centrair", "Chubu"),
    ("KIJ", "Niigata", "Chubu"),
    ("TOY", "Toyama", "Chubu"),
    ("KMQ", "Komatsu", "Chubu"),
    ("FSZ", "Shizuoka", "Chubu"),
    ("ITM", "Osaka Itami", "Kansai"),
    ("KIX", "Kansai International", "Kansai"),
    ("UKB", "Kobe", "Kansai"),
    ("OKJ", "Okayama", "Chugoku"),
    ("HIJ", "Hiroshima", "Chugoku"),
    ("UBJ", "Yamaguchi Ube", "Chugoku"),
    ("IZO", "Izumo", "Chugoku"),
    ("TAK", "Takamatsu", "Shikoku"),
    ("TKS", "Tokushima", "Shikoku"),
    ("MYJ", "Matsuyama", "Shikoku"),
    ("KCZ", "Kochi", "Shikoku"),
    ("KMJ", "Kumamoto", "Kyushu"),
    ("OIT", "Oita", "Kyushu"),
    ("KMI", "Miyazaki", "Kyushu"),
    ("KOJ", "Kagoshima", "Kyushu"),
    ("OKA", "Naha", "Okinawa"),
    ("ISG", "Ishigaki", "Okinawa"),
    ("MMY", "Miyako", "Okinawa"),
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
    ("SKY", "D301", "TYO", "CTS", 1, time(7, 30), timedelta(hours=1, minutes=35)),
    ("WEB", "D302", "HND", "HKD", 1, time(10, 10), timedelta(hours=1, minutes=20)),
    ("SKY", "D303", "NRT", "AKJ", 2, time(12, 25), timedelta(hours=1, minutes=45)),
    ("WEB", "D304", "TYO", "AOJ", 2, time(8, 40), timedelta(hours=1, minutes=20)),
    ("SKY", "D305", "HND", "SDJ", 3, time(9, 20), timedelta(hours=1)),
    ("WEB", "D306", "OSA", "AXT", 3, time(13, 15), timedelta(hours=1, minutes=30)),
    ("SKY", "D307", "NGO", "GAJ", 4, time(11, 5), timedelta(hours=1, minutes=10)),
    ("WEB", "D308", "FUK", "NGO", 4, time(16, 10), timedelta(hours=1, minutes=20)),
    ("SKY", "D309", "NRT", "KIJ", 5, time(7, 55), timedelta(hours=1, minutes=5)),
    ("WEB", "D310", "HND", "TOY", 5, time(12, 40), timedelta(hours=1)),
    ("SKY", "D311", "FUK", "KMQ", 6, time(15, 25), timedelta(hours=1, minutes=20)),
    ("WEB", "D312", "SPK", "FSZ", 7, time(9, 35), timedelta(hours=2)),
    ("SKY", "D313", "FUK", "ITM", 7, time(13, 50), timedelta(hours=1, minutes=10)),
    ("WEB", "D314", "CTS", "KIX", 8, time(8, 20), timedelta(hours=2, minutes=15)),
    ("SKY", "D315", "SDJ", "UKB", 8, time(14, 10), timedelta(hours=1, minutes=30)),
    ("WEB", "D316", "TYO", "OKJ", 9, time(7, 45), timedelta(hours=1, minutes=20)),
    ("SKY", "D317", "CTS", "HIJ", 9, time(11, 30), timedelta(hours=2, minutes=10)),
    ("WEB", "D318", "HND", "UBJ", 10, time(15, 5), timedelta(hours=1, minutes=40)),
    ("SKY", "D319", "TYO", "IZO", 10, time(9, 15), timedelta(hours=1, minutes=25)),
    ("WEB", "D320", "NRT", "TAK", 11, time(12, 20), timedelta(hours=1, minutes=25)),
    ("SKY", "D321", "FUK", "TKS", 11, time(16, 30), timedelta(hours=1)),
    ("WEB", "D322", "HND", "MYJ", 12, time(8, 5), timedelta(hours=1, minutes=30)),
    ("SKY", "D323", "OSA", "KCZ", 12, time(13, 35), timedelta(minutes=50)),
    ("WEB", "D324", "TYO", "KMJ", 13, time(7, 20), timedelta(hours=1, minutes=45)),
    ("SKY", "D325", "OSA", "OIT", 13, time(10, 50), timedelta(hours=1)),
    ("WEB", "D326", "FUK", "KMI", 14, time(14, 25), timedelta(minutes=50)),
    ("SKY", "D327", "SPK", "KOJ", 14, time(9, 40), timedelta(hours=2, minutes=35)),
    ("WEB", "D328", "HND", "OKA", 15, time(6, 55), timedelta(hours=2, minutes=45)),
    ("SKY", "D329", "KIX", "ISG", 15, time(11, 15), timedelta(hours=2, minutes=30)),
    ("WEB", "D330", "NGO", "MMY", 16, time(13, 5), timedelta(hours=2, minutes=35)),
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

    def _validate_seed_data(self):
        city_codes = [code for code, _, _ in CITY_DATA]
        if len(city_codes) != len(set(city_codes)):
            raise CommandError("Seeded destination codes must be unique.")

        airline_codes = [code for code, _ in AIRLINE_DATA]
        if len(airline_codes) != len(set(airline_codes)):
            raise CommandError("Seeded airline codes must be unique.")

        flight_identities = [
            (airline_code, flight_number) for airline_code, flight_number, *_ in FLIGHT_DATA
        ]
        if len(flight_identities) != len(set(flight_identities)):
            raise CommandError("Seeded airline and flight-number identities must be unique.")

        known_city_codes = set(city_codes)
        known_airline_codes = set(airline_codes)
        for (
            airline_code,
            flight_number,
            origin_code,
            destination_code,
            day_offset,
            _,
            duration,
        ) in FLIGHT_DATA:
            if airline_code not in known_airline_codes:
                raise CommandError(f"Seeded flight {flight_number} uses an unknown airline code.")
            if origin_code not in known_city_codes or destination_code not in known_city_codes:
                raise CommandError(
                    f"Seeded flight {flight_number} uses an unknown destination code."
                )
            if origin_code == destination_code:
                raise CommandError(
                    f"Seeded flight {flight_number} must have different origin and "
                    "destination codes."
                )
            if day_offset < 0 or duration <= timedelta(0):
                raise CommandError(f"Seeded flight {flight_number} must have a positive schedule.")

        seat_numbers = [seat_number for seat_number, *_ in SEAT_DATA]
        if len(seat_numbers) != len(set(seat_numbers)):
            raise CommandError("Seeded seat numbers must be unique.")
        if any(price <= 0 for *_, price in SEAT_DATA):
            raise CommandError("Seeded seat prices must be positive.")

    @transaction.atomic
    def handle(self, *args, **options):
        self._validate_seed_data()

        cities = {
            code: City.objects.get_or_create(code=code, defaults={"name": name})[0]
            for code, name, _ in CITY_DATA
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
                Seat.objects.get_or_create(
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
