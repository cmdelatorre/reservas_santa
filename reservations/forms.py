from django import forms

from reservations.models import Reservation
from rooms.models import Room


class ReservationValidationFormMixin(forms.ModelForm):
    """Mixin to validate a reservation: dates and room"""

    def clean(self):
        cleaned_data = super().clean()
        # cc_myself = cleaned_data.get("cc_myself")
        # subject = cleaned_data.get("subject")
        rooms = cleaned_data.get("rooms")
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date >= to_date:
            self.add_error(
                "from_date", "La fecha Desde tiene que ser anterior a la de Hasta"
            )

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
            rooms = ", ".join(
                str(r) for r in Room.objects.filter(id__in=reserved_rooms_ids)
            )
            msg = "Error. En ese período ya se encuentran reservadas: {}".format(rooms)
            self.add_error("rooms", msg)


class MyReservationAdminForm(ReservationValidationFormMixin):
    pass


class ReservationCreationForm(ReservationValidationFormMixin):
    class Meta:
        model = Reservation
        fields = ["from_date", "to_date", "rooms", "notes"]
