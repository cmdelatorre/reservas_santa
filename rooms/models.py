from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=200, verbose_name="nombre de la habitación")

    def __str__(self):
        return self.name

    def filter_reservations(self, start, end):
        """Filter the Room reservations between start (inclusive) and end (exclusive) dates.

        Returns a Reservations Queryset

        """
        return self.reservations.filter(from_date__gte=start, to_date__lte=end)

    class Meta:
        ordering = ["name"]
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
