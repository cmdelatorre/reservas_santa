from django.urls import path

from reservations.views import ReservationsListView

app_name = "profiles"
urlpatterns = [path("", ReservationsListView.as_view(), name="profile")]
