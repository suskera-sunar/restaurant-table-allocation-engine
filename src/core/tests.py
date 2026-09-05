from datetime import date, timedelta

from django.test import TestCase

from ai.allocation import choose_best_table

from .forms import ReservationForm
from .models import Reservation, Table, TimeSlot


class AllocationTests(TestCase):
    def test_chooses_tightest_table(self):
        small = Table.objects.create(number=1, capacity=2, zone="quiet")
        large = Table.objects.create(number=2, capacity=6, zone="window")

        result = choose_best_table(Table.objects.all(), party_size=2)

        self.assertEqual(result, small)
        self.assertNotEqual(result, large)

    def test_rejects_when_no_table_fits(self):
        Table.objects.create(number=1, capacity=2, zone="quiet")

        result = choose_best_table(Table.objects.all(), party_size=4)

        self.assertIsNone(result)

    def test_slot_model_exists_for_admin_setup(self):
        slot = TimeSlot.objects.create(label="6-8 PM", start="18:00", end="20:00")

        self.assertEqual(str(slot), "6-8 PM")

    def test_same_table_can_be_booked_on_different_dates(self):
        table = Table.objects.create(number=1, capacity=2, zone="quiet")
        slot = TimeSlot.objects.create(label="6-8 PM", start="18:00", end="20:00")
        today = date.today()
        Reservation.objects.create(
            guest_name="Today Guest",
            phone="1111111111",
            reservation_date=today,
            party_size=2,
            slot=slot,
            table=table,
        )

        form = ReservationForm(
            data={
                "guest_name": "Tomorrow Guest",
                "phone": "2222222222",
                "reservation_date": today + timedelta(days=1),
                "party_size": 2,
                "slot": slot.pk,
            }
        )

        self.assertTrue(form.is_valid())

    def test_same_phone_cannot_book_same_date_and_slot_twice(self):
        table = Table.objects.create(number=1, capacity=2, zone="quiet")
        slot = TimeSlot.objects.create(label="6-8 PM", start="18:00", end="20:00")
        reservation_date = date.today()
        Reservation.objects.create(
            guest_name="First Guest",
            phone="9999999999",
            reservation_date=reservation_date,
            party_size=2,
            slot=slot,
            table=table,
        )

        form = ReservationForm(
            data={
                "guest_name": "Second Guest",
                "phone": "9999999999",
                "reservation_date": reservation_date,
                "party_size": 2,
                "slot": slot.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("already has a reservation", str(form.errors))

    def test_phone_formatting_cannot_bypass_duplicate_check(self):
        table = Table.objects.create(number=1, capacity=2, zone="quiet")
        slot = TimeSlot.objects.create(label="6-8 PM", start="18:00", end="20:00")
        Reservation.objects.create(
            guest_name="First Guest",
            phone="9876543210",
            reservation_date=date.today(),
            party_size=2,
            slot=slot,
            table=table,
        )

        form = ReservationForm(
            data={
                "guest_name": "Second Guest",
                "phone": "987-654-3210",
                "reservation_date": date.today(),
                "party_size": 2,
                "slot": slot.pk,
            }
        )

        self.assertFalse(form.is_valid())
