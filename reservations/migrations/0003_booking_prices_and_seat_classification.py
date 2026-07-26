from decimal import ROUND_HALF_UP, Decimal

import django.core.validators
from django.db import migrations, models

import reservations.models


def classify_and_price_existing_rows(apps, schema_editor):
    Seat = apps.get_model("reservations", "Seat")
    Booking = apps.get_model("reservations", "Booking")

    for seat in Seat.objects.all().iterator():
        seat_letter = seat.seat_number.strip().upper()[-1:]
        if seat_letter in {"A", "F"}:
            seat_type = "WINDOW"
        elif seat_letter in {"B", "E"}:
            seat_type = "MIDDLE"
        else:
            seat_type = "AISLE"
        seat.cabin_class = "ECONOMY"
        seat.seat_type = seat_type
        seat.price = Decimal("15000")
        seat.save(update_fields=["cabin_class", "seat_type", "price"])

    used_references = set(
        Booking.objects.exclude(booking_reference__isnull=True).values_list(
            "booking_reference", flat=True
        )
    )
    for booking in Booking.objects.select_related("seat").all().iterator():
        taxes_and_fees = (booking.seat.price * Decimal("0.10")).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
        reference = reservations.models.generate_booking_reference()
        while reference in used_references:
            reference = reservations.models.generate_booking_reference()
        used_references.add(reference)
        booking.base_fare = booking.seat.price
        booking.taxes_and_fees = taxes_and_fees
        booking.total_price = booking.seat.price + taxes_and_fees
        booking.booking_reference = reference
        booking.save(
            update_fields=[
                "base_fare",
                "taxes_and_fees",
                "total_price",
                "booking_reference",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0002_booking_booking_has_user_or_guest_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="seat",
            name="cabin_class",
            field=models.CharField(
                choices=[("ECONOMY", "Economy"), ("BUSINESS", "Business")],
                default="ECONOMY",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="seat",
            name="seat_type",
            field=models.CharField(
                choices=[("WINDOW", "Window"), ("MIDDLE", "Middle"), ("AISLE", "Aisle")],
                default="AISLE",
                max_length=6,
            ),
        ),
        migrations.AddField(
            model_name="seat",
            name="price",
            field=models.DecimalField(
                decimal_places=0,
                default=Decimal("15000"),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="base_fare",
            field=models.DecimalField(
                decimal_places=0,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="taxes_and_fees",
            field=models.DecimalField(
                decimal_places=0,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="total_price",
            field=models.DecimalField(
                decimal_places=0,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="booking_reference",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.RunPython(classify_and_price_existing_rows, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="booking",
            name="base_fare",
            field=models.DecimalField(
                decimal_places=0,
                default=Decimal("0"),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="taxes_and_fees",
            field=models.DecimalField(
                decimal_places=0,
                default=Decimal("0"),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="total_price",
            field=models.DecimalField(
                decimal_places=0,
                default=Decimal("0"),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="booking_reference",
            field=models.CharField(
                default=reservations.models.generate_booking_reference,
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
    ]
