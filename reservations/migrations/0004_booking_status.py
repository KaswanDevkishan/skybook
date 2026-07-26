from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0003_booking_prices_and_seat_classification"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[("CONFIRMED", "Confirmed"), ("CANCELLED", "Cancelled")],
                default="CONFIRMED",
                max_length=9,
            ),
        ),
        migrations.RemoveConstraint(
            model_name="booking",
            name="unique_booking_per_seat",
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.UniqueConstraint(
                condition=models.Q(("status", "CONFIRMED")),
                fields=("seat",),
                name="unique_confirmed_booking_per_seat",
            ),
        ),
    ]
