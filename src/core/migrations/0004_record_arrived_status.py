from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_arrived_status_constraint"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("confirmed", "Confirmed"),
                    ("arrived", "Arrived"),
                    ("cancelled", "Cancelled"),
                    ("no_show", "No-show"),
                ],
                default="confirmed",
                max_length=20,
            ),
        ),
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
