from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

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

    def test_guest_name_accepts_names_but_rejects_numbers(self):
        slot = TimeSlot.objects.create(label="6-8 PM", start="18:00", end="20:00")
        valid_form = ReservationForm(
            data={
                "guest_name": "Mary-Jane O'Neil",
                "phone": "1234567890",
                "reservation_date": date.today(),
                "party_size": 2,
                "slot": slot.pk,
            }
        )
        invalid_form = ReservationForm(
            data={
                "guest_name": "Guest 42",
                "phone": "1234567890",
                "reservation_date": date.today(),
                "party_size": 2,
                "slot": slot.pk,
            }
        )

        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("Guest name can contain", str(invalid_form.errors))

    def test_party_size_must_be_at_least_two(self):
        slot = TimeSlot.objects.create(label="Morning", start="09:00", end="12:00")
        form = ReservationForm(
            data={
                "guest_name": "Solo Guest",
                "phone": "1234567890",
                "reservation_date": date.today(),
                "party_size": 1,
                "slot": slot.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("at least 2", str(form.errors))

    def test_party_size_cannot_exceed_largest_active_table(self):
        table = Table.objects.create(number=1, capacity=4, zone="quiet")
        slot = TimeSlot.objects.create(label="Evening", start="18:00", end="21:00")
        form = ReservationForm(
            data={
                "guest_name": "Large Party",
                "phone": "1234567890",
                "reservation_date": date.today(),
                "party_size": 5,
                "slot": slot.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("largest table seats 4", str(form.errors))
        self.assertEqual(form.fields["party_size"].widget.attrs["max"], 4)

    def test_staff_dashboard_marks_reserved_table_full_for_slot(self):
        staff_user = User.objects.create_user(
            username="staff", password="test-password", is_staff=True
        )
        self.client.force_login(staff_user)
        table = Table.objects.create(number=1, capacity=2, zone="quiet")
        other_table = Table.objects.create(number=2, capacity=4, zone="window")
        slot = TimeSlot.objects.create(label="6-8 PM", start="18:00", end="20:00")
        Reservation.objects.create(
            guest_name="Reserved Guest",
            phone="1234567890",
            reservation_date=date.today(),
            party_size=2,
            slot=slot,
            table=table,
        )

        response = self.client.get("/staff/", {"date": date.today().isoformat()})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Table 1")
        self.assertContains(response, "Full · 2 seats")
        self.assertContains(response, f"Available · {other_table.capacity} seats")

    def test_booking_creates_one_allocation_per_selected_slot(self):
        Table.objects.create(number=1, capacity=4, zone="quiet")
        morning = TimeSlot.objects.create(label="Morning", start="09:00", end="12:00")
        evening = TimeSlot.objects.create(label="Evening", start="18:00", end="21:00")

        response = self.client.post(
            "/",
            {
                "guest_name": "Multi Slot Guest",
                "phone": "1234567890",
                "reservation_date": date.today().isoformat(),
                "party_size": 2,
                "slots": [morning.pk, evening.pk],
            },
        )

        self.assertRedirects(response, "/")
        self.assertEqual(Reservation.objects.count(), 2)
        self.assertSetEqual(
            set(Reservation.objects.values_list("slot_id", flat=True)),
            {morning.pk, evening.pk},
        )

    def test_phone_number_requires_ten_digits(self):
        slot = TimeSlot.objects.create(label="Morning", start="09:00", end="12:00")
        form = ReservationForm(
            data={
                "guest_name": "Phone Guest",
                "phone": "986695427",
                "reservation_date": date.today(),
                "party_size": 2,
                "slots": [slot.pk],
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("10 digits", str(form.errors))
