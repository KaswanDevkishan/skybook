import secrets
import string
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Length, Trim
from django.db.models.lookups import GreaterThan

BOOKING_REFERENCE_ALPHABET = "".join(
    character for character in string.ascii_uppercase + string.digits if character not in "0O1I"
)


def generate_booking_reference():
    suffix = "".join(secrets.choice(BOOKING_REFERENCE_ALPHABET) for _ in range(8))
    return f"SKY-{suffix}"


class City(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name_plural = "cities"
        ordering = ["code"]

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ["code"]

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Flight(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.PROTECT, related_name="flights")
    flight_number = models.CharField(max_length=10)
    origin = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="departing_flights",
    )
    destination = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="arriving_flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["departure_time", "airline__code", "flight_number"]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(origin=models.F("destination")),
                name="flight_origin_destination_differ",
            ),
            models.CheckConstraint(
                condition=models.Q(arrival_time__gt=models.F("departure_time")),
                name="flight_arrival_after_departure",
            ),
            models.UniqueConstraint(
                fields=["airline", "flight_number", "departure_time"],
                name="unique_scheduled_flight",
            ),
        ]

    def __str__(self):
        return (
            f"{self.airline.code}{self.flight_number}: {self.origin.code} → {self.destination.code}"
        )

    @property
    def duration(self):
        return self.arrival_time - self.departure_time


class Seat(models.Model):
    class CabinClass(models.TextChoices):
        ECONOMY = "ECONOMY", "Economy"
        BUSINESS = "BUSINESS", "Business"

    class SeatType(models.TextChoices):
        WINDOW = "WINDOW", "Window"
        MIDDLE = "MIDDLE", "Middle"
        AISLE = "AISLE", "Aisle"

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=5)
    cabin_class = models.CharField(
        max_length=10,
        choices=CabinClass.choices,
        default=CabinClass.ECONOMY,
    )
    seat_type = models.CharField(
        max_length=6,
        choices=SeatType.choices,
        default=SeatType.AISLE,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=Decimal("15000"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    class Meta:
        ordering = ["flight", "seat_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["flight", "seat_number"],
                name="unique_seat_per_flight",
            )
        ]

    def save(self, *args, **kwargs):
        self.seat_number = self.seat_number.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flight} — seat {self.seat_number}"

    @property
    def seat_row(self):
        return self.seat_number.rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ") or self.seat_number


class Booking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name="bookings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="bookings",
        blank=True,
        null=True,
    )
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    base_fare = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    taxes_and_fees = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    booking_reference = models.CharField(
        max_length=12,
        unique=True,
        default=generate_booking_reference,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["seat"], name="unique_booking_per_seat"),
            models.CheckConstraint(
                condition=(
                    models.Q(user__isnull=False)
                    | (
                        GreaterThan(Length(Trim("guest_name")), 0)
                        & GreaterThan(Length(Trim("guest_email")), 0)
                    )
                ),
                name="booking_has_user_or_guest_details",
            ),
        ]

    def clean(self):
        super().clean()
        if self.user_id is None and (not self.guest_name.strip() or not self.guest_email.strip()):
            raise ValidationError("Guest bookings require a guest name and email address.")

    def save(self, *args, **kwargs):
        if self._state.adding and not any((self.base_fare, self.taxes_and_fees, self.total_price)):
            from reservations.pricing import calculate_booking_price

            price = calculate_booking_price(self.seat.price)
            self.base_fare = price.base_fare
            self.taxes_and_fees = price.taxes_and_fees
            self.total_price = price.total_price
        super().save(*args, **kwargs)

    def __str__(self):
        passenger = self.user.get_username() if self.user else self.guest_name
        return f"{self.booking_reference}: {self.seat} booked for {passenger}"
