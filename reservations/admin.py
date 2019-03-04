from django import forms
from django.contrib import admin
from .models import Reservation
from rooms.models import Room


class MyReservationAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        # cc_myself = cleaned_data.get("cc_myself")
        # subject = cleaned_data.get("subject")
        rooms = cleaned_data.get("rooms")
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if self.instance:
            reservations = Reservation.objects.exclude(id=self.instance.id)
        else:
            reservations = Reservation.objects.all()

        potential_conflicts = reservations.filter(
            to_date__gt=from_date, from_date__lt=to_date
        )

        reserved_rooms_ids = set(
            potential_conflicts.values_list("rooms__id", flat=True)
        )
        conflicting_rooms = reserved_rooms_ids.intersection(
            set(rooms.values_list("id", flat=True))
        )

        if conflicting_rooms:
            rooms = [str(r) for r in Room.objects.filter(id__in=conflicting_rooms)]
            msg = "Invalid rooms selection. Rooms already reserved for the period: {}".format(
                rooms
            )
            self.add_error("rooms", msg)


class ReservationAdmin(admin.ModelAdmin):
    form = MyReservationAdminForm
    list_display = ["user", "from_date", "to_date", "rooms_list", "notes"]
    list_display_links = ("from_date", "to_date", "rooms_list")

    def rooms_list(self, res):
        return ", ".join(map(lambda x: x[0], res.rooms.all().values_list("name")))


admin.site.register(Reservation, ReservationAdmin)
