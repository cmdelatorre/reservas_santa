import django

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _


UserModel = get_user_model()


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """

    email = forms.EmailField(
        label=_("Email address"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label=_("Password"), strip=False, widget=forms.PasswordInput
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                if django.VERSION < (2, 1):
                    raise forms.ValidationError(
                        self.error_messages["invalid_login"],
                        code="invalid_login",
                        params={"username": self.username_field.verbose_name},
                    )

                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"], code="inactive"
            )

    if django.VERSION < (2, 1):

        def get_user_id(self):
            if self.user_cache:
                return self.user_cache.id
            return None

    def get_user(self):
        return self.user_cache

    if django.VERSION >= (2, 1):

        def get_invalid_login_error(self):
            return forms.ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )
