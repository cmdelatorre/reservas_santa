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
    path("nueva/", ReservationCreate.as_view(), name="create"),
    path("editar/<int:pk>/", ReservationEdit.as_view(), name="edit"),
    path("cancelar/<int:pk>/", ReservationDelete.as_view(), name="delete"),
    path("eventos/<int:room_id>/", RoomReservations.as_view(), name="events"),
]
