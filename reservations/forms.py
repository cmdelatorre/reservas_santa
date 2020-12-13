from datetime import datetime, date, timedelta
from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationFormUniqueEmail

from reservations.models import Reservation
from rooms.models import Room


CustomUser = get_user_model()


class MyCustomUserForm(RegistrationFormUniqueEmail):

    first_name = forms.CharField(
        max_length=64,
        required=True,
        help_text="Requerido, por favor poné tu nombre",
        label="Nombre",
    )
    last_name = forms.CharField(
        max_length=64,
        required=True,
        help_text="Requerido, por favor poné tu apellido",
        label="Apellido",
    )

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2")
        help_texts = {
            "email": "Requerida. Luego será usada para entrar al sitio.",
            "password1": "No te preocupes: si te la olvidas podrás recuperarla.",
            "password2": "La misma que pusiste antes (para asegurarnos que la escribiste bien)",
        }
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Dirección de email",
            "password1": "Contraseña",
            "password2": "Repetir contraseña",
        }


class ReservationValidationFormMixin(forms.ModelForm):
    """Mixin to validate a reservation: dates and room"""

    def clean(self):
        cleaned_data = super().clean()
        if len(self.errors):
            return
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
            msg = "En ese período hay conflictos con reservas de: {}".format(rooms)
            self.add_error("rooms", msg)


class MyReservationAdminForm(ReservationValidationFormMixin):
    pass


class ReservationCreationForm(ReservationValidationFormMixin):
    from_date = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="Fecha de la primer noche",
        required=True,
    )
    to_date = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="Fecha de salida (esa noche no se usa habitación)",
        required=True,
    )

    class Meta:
        model = Reservation
        # fields = ["from_date", "to_date", "rooms", "notes"]
        exclude = ("user",)
        help_texts = {
            "from_date": "Fecha de la primer noche",
            "to_date": "Fecha de salida (esa noche no se usa habitación)",
            "rooms": "Seleccione múltiples habitaciones dejando apretado Ctrl",
            "notes": "Opcional. Cualquier mensaje que consideres oportuno.",
        }


TARGET_YEAR = datetime.now().year + 1
TURNS_START = date(TARGET_YEAR, 1, 1)


class TurnsPreparationForm(forms.Form):
    """Form for the definition of holiday turns."""

    year = forms.IntegerField(
        label="Año para el que calcular los turnos",
        required=True,
        min_value=2000,
        max_value=2100,
        initial=TARGET_YEAR,
    )
    date_start = forms.DateField(
        label="Día concreto en que empieza el primer turno",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=TURNS_START,
    )
    turn_length = forms.IntegerField(
        label="Largo (en días) deseado para cada turno",
        required=True,
        min_value=1,
        max_value=365,
        initial=8,
    )


class TurnsCreationForm(forms.Form):
    """Form for the creation of holiday turns"""

    year = forms.IntegerField(
        label="Año para el que calcular los turnos",
        required=True,
        widget=forms.widgets.Input(attrs={"readonly": True}),
    )
    date_start = forms.DateField(
        label="Día concreto en que empieza el primer turno",
        required=True,
        widget=forms.widgets.Input(attrs={"readonly": True}),
    )
    turn_length = forms.IntegerField(
        label="Largo (en días) deseado para cada turno",
        required=True,
        widget=forms.widgets.Input(attrs={"readonly": True}),
    )
