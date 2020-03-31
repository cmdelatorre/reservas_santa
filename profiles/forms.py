from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import validators

from profiles.models import Profile


CustomUser = get_user_model()


class UserProfileForm(forms.ModelForm):

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
    wants_emails = forms.BooleanField(
        required=False,
        help_text="¿Querés recibir un email por CADA reserva que se haga (cualquier persona)?",
        label="¿recibir emails?",
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "wants_emails")
        help_texts = {"email": "Requerida. Luego será usada para entrar al sitio."}
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Dirección de email",
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        email_field = CustomUser.get_email_field_name()
        self.fields[email_field].validators.append(
            validators.CaseInsensitiveUnique(
                CustomUser, email_field, validators.DUPLICATE_EMAIL
            )
        )
