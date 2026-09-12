from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.booking, name="booking"),
    path("allocation/<int:slot_id>/", views.allocation_board, name="allocation-board"),
    path("staff/", views.staff_dashboard, name="staff-dashboard"),
]
