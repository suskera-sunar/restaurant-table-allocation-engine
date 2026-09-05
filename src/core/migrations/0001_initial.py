from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Table",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.PositiveIntegerField(unique=True)),
                ("capacity", models.PositiveIntegerField()),
                ("zone", models.CharField(blank=True, max_length=80)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["capacity", "number"]},
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=80, unique=True)),
                ("start", models.TimeField()),
                ("end", models.TimeField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["start"]},
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guest_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30)),
                ("party_size", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("confirmed", "Confirmed"), ("cancelled", "Cancelled"), ("no_show", "No-show")], default="confirmed", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("slot", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservations", to="core.timeslot")),
                ("table", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="reservations", to="core.table")),
            ],
            options={"ordering": ["slot", "table__number", "created_at"]},
        ),
    ]
