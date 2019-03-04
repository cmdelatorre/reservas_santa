from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    name = "reservations"
    verbose_name = "Reservas"

    def ready(self):
        from reservations.signals import validate_reservation

        print("algo")
