from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ["user", "from_date", "to_date", "rooms_list", "notes"]

    def rooms_list(self, res):
        return ", ".join(map(lambda x: x[0], res.rooms.all().values_list("name")))


admin.site.register(Reservation, ReservationAdmin)
