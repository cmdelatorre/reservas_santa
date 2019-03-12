from django.urls import path

from reservations.views import ReservationsListView, ReservationCreate, RoomReservations

app_name = "reservations"
urlpatterns = [
    path("", ReservationsListView.as_view(), name="index"),
    path("nueva_reserva/", ReservationCreate.as_view(), name="create"),
    path("events/<int:room_id>/", RoomReservations.as_view(), name="events"),
]
