from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_reservation_date_and_duplicate_constraint"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="reservation",
            name="one_confirmed_booking_per_phone_slot",
        ),
        migrations.AddConstraint(
            model_name="reservation",
            constraint=models.UniqueConstraint(
                condition=Q(status__in=["confirmed", "arrived"]),
                fields=("phone", "reservation_date", "slot"),
                name="one_confirmed_booking_per_phone_slot",
            ),
        ),
    ]
