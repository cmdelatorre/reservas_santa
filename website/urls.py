"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from reservations.views import ReservationsListView

admin.autodiscover()

from django import forms

from django_registration.backends.activation.views import RegistrationView
from django_registration.forms import RegistrationForm


class MyCustomUserForm(RegistrationForm):

    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta(RegistrationForm.Meta):
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ReservationsListView.as_view()),
    path("", include("reservations.urls", namespace="reservations")),
    path(
        r"usuarios/register/",
        RegistrationView.as_view(form_class=MyCustomUserForm),
        name="django_registration_register",
    ),
    path("usuarios/", include("django_registration.backends.activation.urls")),
    path("usuarios/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
