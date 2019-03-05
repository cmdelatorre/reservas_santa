from django.urls import path

from reservations.views import ReservationsListView, ReservationCreate

app_name = "reservations"
urlpatterns = [
    path("", ReservationsListView.as_view(), name="index"),
    path("nueva_reserva/", ReservationCreate.as_view(), name="create"),
]
