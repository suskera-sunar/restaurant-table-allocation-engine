from django.db import models


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    zone = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["capacity", "number"]

    def __str__(self):
        return f"Table {self.number} ({self.capacity} seats)"


class TimeSlot(models.Model):
    label = models.CharField(max_length=80, unique=True)
    start = models.TimeField()
    end = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["start"]

    def __str__(self):
        return self.label


class Reservation(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        ARRIVED = "arrived", "Arrived"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No-show"

    guest_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    reservation_date = models.DateField()
    party_size = models.PositiveIntegerField()
    slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name="reservations")
    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="reservations",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["reservation_date", "slot", "table__number", "created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["phone", "reservation_date", "slot"],
                condition=models.Q(status__in=["confirmed", "arrived"]),
                name="one_confirmed_booking_per_phone_slot",
            )
        ]

    def __str__(self):
        return f"{self.guest_name} ({self.party_size}) - {self.reservation_date} - {self.slot}"
