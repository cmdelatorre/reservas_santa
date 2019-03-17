from django.urls import path

from reservations.views import (
    ReservationsListView,
    ReservationCreate,
    RoomReservations,
    ReservationEdit,
    ReservationDelete,
)

app_name = "reservations"
urlpatterns = [
    path("", ReservationsListView.as_view(), name="index"),
    path("nueva_reserva/", ReservationCreate.as_view(), name="create"),
    path("editar_reserva/<int:pk>/", ReservationEdit.as_view(), name="edit"),
    path("cancelar_reserva/<int:pk>/", ReservationDelete.as_view(), name="delete"),
    path("events/<int:room_id>/", RoomReservations.as_view(), name="events"),
]
