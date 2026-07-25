from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


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


class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=5)

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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["seat"], name="unique_booking_per_seat"),
        ]

    def clean(self):
        super().clean()
        if self.user_id is None and (not self.guest_name.strip() or not self.guest_email.strip()):
            raise ValidationError("Guest bookings require a guest name and email address.")

    def __str__(self):
        passenger = self.user.get_username() if self.user else self.guest_name
        return f"{self.seat} booked for {passenger}"
