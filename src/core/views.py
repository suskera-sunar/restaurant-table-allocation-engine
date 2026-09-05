from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from ai.allocation import choose_best_table

from .forms import ReservationForm
from .models import Reservation, Table, TimeSlot


@transaction.atomic
def booking(request):
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        reservation = form.save(commit=False)
        occupied_ids = Reservation.objects.filter(
            reservation_date=reservation.reservation_date,
            slot=reservation.slot,
            status__in=[Reservation.Status.CONFIRMED, Reservation.Status.ARRIVED],
            table__isnull=False,
        ).values_list("table_id", flat=True)
        table = choose_best_table(
            Table.objects.filter(is_active=True),
            reservation.party_size,
            occupied_table_ids=occupied_ids,
        )
        if table is None:
            form.add_error(None, "No suitable table is available for this time slot.")
        else:
            reservation.table = table
            reservation.save()
            messages.success(
                request,
                f"Reservation confirmed for {reservation.reservation_date} at "
                f"{reservation.slot} on Table {table.number}.",
            )
            return redirect("core:booking")

    return render(request, "core/booking.html", {"form": form})


def allocation_board(request, slot_id):
    slot = get_object_or_404(TimeSlot, pk=slot_id)
    reservation_date = request.GET.get("date")
    reservations = Reservation.objects.filter(slot=slot).select_related("table")
    if reservation_date:
        reservations = reservations.filter(reservation_date=reservation_date)
    return render(
        request,
        "core/allocation_board.html",
        {"slot": slot, "reservations": reservations, "reservation_date": reservation_date},
    )
