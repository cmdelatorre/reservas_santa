from django.contrib import admin

from reservations.models import Reservation
from reservations.forms import MyReservationAdminForm
from rooms.models import Room


class ReservationAdmin(admin.ModelAdmin):
    form = MyReservationAdminForm
    list_display = ["user", "from_date", "to_date", "rooms_list", "notes"]
    list_display_links = ("from_date", "to_date", "rooms_list")

    def rooms_list(self, res):
        return ", ".join(map(lambda x: x[0], res.rooms.all().values_list("name")))


admin.site.register(Reservation, ReservationAdmin)
