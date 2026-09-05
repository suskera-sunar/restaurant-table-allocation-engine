from django import forms
from django.utils import timezone

from .models import Reservation, TimeSlot


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["guest_name", "phone", "reservation_date", "party_size", "slot"]
        widgets = {
            "guest_name": forms.TextInput(attrs={"placeholder": "Guest name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number"}),
            "reservation_date": forms.DateInput(attrs={"type": "date"}),
            "party_size": forms.NumberInput(attrs={"min": 1, "max": 50}),
            "slot": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = TimeSlot.objects.filter(is_active=True)
        self.fields["reservation_date"].initial = timezone.localdate()
        self.fields["reservation_date"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data["reservation_date"]
        if reservation_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return reservation_date

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        normalized_phone = "".join(character for character in phone if character.isdigit())
        if len(normalized_phone) < 7:
            raise forms.ValidationError("Enter a valid phone number.")
        return normalized_phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        reservation_date = cleaned_data.get("reservation_date")
        slot = cleaned_data.get("slot")
        if phone and reservation_date and slot:
            duplicate = Reservation.objects.filter(
                phone=phone,
                reservation_date=reservation_date,
                slot=slot,
                status__in=[Reservation.Status.CONFIRMED, Reservation.Status.ARRIVED],
            ).exists()
            if duplicate:
                raise forms.ValidationError(
                    "This phone number already has a reservation for this date and time slot."
                )
        return cleaned_data
