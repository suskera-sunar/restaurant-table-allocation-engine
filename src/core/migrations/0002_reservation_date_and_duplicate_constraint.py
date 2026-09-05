from django.db import migrations, models
from django.db.models import Q


def cancel_duplicate_confirmed_bookings(apps, schema_editor):
    Reservation = apps.get_model("core", "Reservation")
    seen = set()
    duplicates = []
    reservations = Reservation.objects.filter(status__in=["confirmed", "arrived"]).order_by(
        "phone", "reservation_date", "slot_id", "created_at", "id"
    )
    for reservation in reservations:
        key = (reservation.phone, reservation.reservation_date, reservation.slot_id)
        if key in seen:
            duplicates.append(reservation.id)
        else:
            seen.add(key)
    Reservation.objects.filter(id__in=duplicates).update(status="cancelled", table=None)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="reservation_date",
            field=models.DateField(default="2026-09-05"),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="reservation",
            options={"ordering": ["reservation_date", "slot", "table__number", "created_at"]},
        ),
        migrations.RunPython(cancel_duplicate_confirmed_bookings, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="reservation",
            constraint=models.UniqueConstraint(
                condition=Q(status__in=["confirmed", "arrived"]),
                fields=("phone", "reservation_date", "slot"),
                name="one_confirmed_booking_per_phone_slot",
            ),
        ),
    ]
