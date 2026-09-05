from django.contrib import admin

from .models import Reservation, Table, TimeSlot


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["number", "capacity", "zone", "is_active"]
    list_filter = ["zone", "is_active"]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ["label", "start", "end", "is_active"]
    list_filter = ["is_active"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["guest_name", "reservation_date", "party_size", "slot", "table", "status", "created_at"]
    list_filter = ["reservation_date", "slot", "status"]
    search_fields = ["guest_name", "phone"]
