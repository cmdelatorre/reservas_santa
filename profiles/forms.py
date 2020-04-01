from django import forms
from django.contrib.auth import get_user_model


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
        user_fields = ("first_name", "last_name")
        model = CustomUser
        fields = user_fields + ("wants_emails",)
        labels = {"first_name": "Nombre", "last_name": "Apellido"}

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        do_save_user = False
        for field_name in self.Meta.user_fields:
            if getattr(profile.user, field_name) != self.cleaned_data[field_name]:
                setattr(profile.user, field_name, self.cleaned_data[field_name])
                do_save_user = True
        if do_save_user:
            profile.user.save()
        return profile
