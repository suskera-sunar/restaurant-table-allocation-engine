from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ai.allocation import choose_best_table

from .forms import ReservationForm
from .models import Reservation, Table, TimeSlot


@transaction.atomic
def booking(request):
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        reservation = form.save(commit=False)
        selected_slots = list(form.cleaned_data["slots"])
        tables = Table.objects.filter(is_active=True)
        allocations = []
        for slot in selected_slots:
            occupied_ids = Reservation.objects.filter(
                reservation_date=reservation.reservation_date,
                slot=slot,
                status__in=[Reservation.Status.CONFIRMED, Reservation.Status.ARRIVED],
                table__isnull=False,
            ).values_list("table_id", flat=True)
            table = choose_best_table(
                tables,
                reservation.party_size,
                occupied_table_ids=occupied_ids,
            )
            if table is None:
                form.add_error(
                    None,
                    f"No suitable table is available for the {slot.label} period. "
                    "Choose fewer periods or another date.",
                )
                break
            allocations.append((slot, table))
        else:
            for slot, table in allocations:
                Reservation.objects.create(
                    guest_name=reservation.guest_name,
                    phone=reservation.phone,
                    reservation_date=reservation.reservation_date,
                    party_size=reservation.party_size,
                    slot=slot,
                    table=table,
                )
            messages.success(
                request,
                f"Reservation confirmed for {reservation.reservation_date} across "
                f"{len(allocations)} dining period(s).",
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


@staff_member_required
def staff_dashboard(request):
    reservation_date = request.GET.get("date") or timezone.localdate().isoformat()
    try:
        selected_date = timezone.datetime.strptime(reservation_date, "%Y-%m-%d").date()
    except ValueError:
        selected_date = timezone.localdate()
        reservation_date = selected_date.isoformat()

    slots = list(TimeSlot.objects.filter(is_active=True))
    tables = list(Table.objects.filter(is_active=True))
    reservations = Reservation.objects.filter(
        reservation_date=selected_date,
        status__in=[Reservation.Status.CONFIRMED, Reservation.Status.ARRIVED],
    ).select_related("slot", "table")
    reservations_by_slot = {slot.id: [] for slot in slots}
    for reservation in reservations:
        reservations_by_slot.setdefault(reservation.slot_id, []).append(reservation)

    slot_rows = []
    for slot in slots:
        slot_reservations = reservations_by_slot.get(slot.id, [])
        occupied_ids = {reservation.table_id for reservation in slot_reservations if reservation.table_id}
        slot_rows.append(
            {
                "slot": slot,
                "reservations": slot_reservations,
                "occupied_ids": occupied_ids,
                "available_count": sum(table.id not in occupied_ids for table in tables),
            }
        )

    return render(
        request,
        "core/staff_dashboard.html",
        {
            "selected_date": selected_date,
            "reservation_date": reservation_date,
            "tables": tables,
            "slot_rows": slot_rows,
        },
    )
