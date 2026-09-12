import re

from django import forms
from django.db.models import Max
from django.utils import timezone

from .models import Reservation, Table, TimeSlot


class SlotMultipleChoiceField(forms.ModelMultipleChoiceField):
    def to_python(self, value):
        if value and isinstance(value, (str, int)):
            value = [value]
        return super().to_python(value)


class ReservationForm(forms.ModelForm):
    slots = SlotMultipleChoiceField(
        queryset=TimeSlot.objects.none(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "slot-select",
                "data-placeholder": "Choose one or more dining periods",
            }
        ),
        label="Dining periods",
        help_text="Select one or more periods.",
    )

    class Meta:
        model = Reservation
        fields = ["guest_name", "phone", "reservation_date", "party_size", "slots"]
        widgets = {
            "guest_name": forms.TextInput(
                attrs={
                    "placeholder": "Guest name",
                    "maxlength": 120,
                    "pattern": r"[A-Za-z][A-Za-z '\-]*",
                    "title": "Use letters, spaces, apostrophes, or hyphens only.",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Mobile number (10 digits)",
                    "type": "tel",
                    "inputmode": "numeric",
                    "maxlength": 10,
                    "pattern": r"[0-9]{10}",
                }
            ),
            "reservation_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "text", "class": "datepicker", "autocomplete": "off"},
            ),
            "party_size": forms.NumberInput(attrs={"min": 2, "max": 50}),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get("data") is not None and "slot" in kwargs["data"] and "slots" not in kwargs["data"]:
            data = kwargs["data"].copy()
            if hasattr(data, "setlist"):
                data.setlist("slots", data.getlist("slot"))
            else:
                data["slots"] = [data["slot"]]
            kwargs["data"] = data
        super().__init__(*args, **kwargs)
        self.fields["party_size"].min_value = 2
        self.fields["slots"].queryset = TimeSlot.objects.filter(is_active=True)
        self.fields["reservation_date"].initial = timezone.localdate()
        self.fields["reservation_date"].widget.attrs["min"] = timezone.localdate().isoformat()
        largest_table = Table.objects.filter(is_active=True).aggregate(
            max_capacity=Max("capacity")
        )["max_capacity"]
        if largest_table:
            self.fields["party_size"].widget.attrs["max"] = largest_table

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data["reservation_date"]
        if reservation_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return reservation_date

    def clean_guest_name(self):
        guest_name = " ".join(self.cleaned_data["guest_name"].split())
        if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]*", guest_name):
            raise forms.ValidationError(
                "Guest name can contain letters, spaces, apostrophes, and hyphens only."
            )
        return guest_name

    def clean_party_size(self):
        party_size = self.cleaned_data["party_size"]
        if party_size < 2:
            raise forms.ValidationError("Bookings require a party of at least 2 people.")
        largest_table = Table.objects.filter(is_active=True).aggregate(
            max_capacity=Max("capacity")
        )["max_capacity"]
        if largest_table is not None and party_size > largest_table:
            raise forms.ValidationError(
                f"Our largest table seats {largest_table} people. "
                "Please reduce your party size or contact the restaurant."
            )
        return party_size

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        normalized_phone = "".join(character for character in phone if character.isdigit())
        if len(normalized_phone) != 10:
            raise forms.ValidationError("Enter a valid mobile number with 10 digits.")
        return normalized_phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        reservation_date = cleaned_data.get("reservation_date")
        slots = cleaned_data.get("slots")
        if phone and reservation_date and slots:
            duplicate = Reservation.objects.filter(
                phone=phone,
                reservation_date=reservation_date,
                slot__in=slots,
                status__in=[Reservation.Status.CONFIRMED, Reservation.Status.ARRIVED],
            ).exists()
            if duplicate:
                raise forms.ValidationError(
                    "This phone number already has a reservation for this date and time slot."
                )
        return cleaned_data
