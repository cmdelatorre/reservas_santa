from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    name = "reservations"
    verbose_name = "Reservas"

    def ready(self):
        from .signals import *
