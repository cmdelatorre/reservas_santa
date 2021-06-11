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
from cuser.forms import AuthenticationForm
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.generic import TemplateView
from django_registration.backends.activation.views import RegistrationView

from .fuel import fetch_fuel_price
from reservations.forms import MyCustomUserForm


admin.autodiscover()


def doc_view():
    fuel_price = fetch_fuel_price()
    nightly_cost = round(2.5 * fuel_price)
    do_format = lambda s: ("%.2f" % s).replace(".", ",")  # 12,34
    return TemplateView.as_view(
        template_name="doc.html",
        extra_context={
            "fuel_price": do_format(fuel_price),
            "nightly_cost": nightly_cost,
        },
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("generalidades/", doc_view(), name="doc"),
    path("reservas/", include("reservations.urls", namespace="reservations")),
    path("preferencias/", include("profiles.urls", namespace="profiles")),
    path(
        "usuarios/register/",
        RegistrationView.as_view(form_class=MyCustomUserForm),
        name="django_registration_register",
    ),
    path("usuarios/", include("django_registration.backends.activation.urls")),
    path(
        "usuarios/login/",
        LoginView.as_view(authentication_form=AuthenticationForm),
        name="login",
    ),
    path("usuarios/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
