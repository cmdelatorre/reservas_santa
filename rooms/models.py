from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=200, verbose_name="nombre de la habitación")

    def __str__(self):
        return self.name

    def filter_reservations_that_intersect(self, start, end):
        """Filter the Room reservations that intersect with the given period.

        Returns a Reservations Queryset

        """
        return self.reservations.exclude(to_date__gt=end).exclude(to_date__lte=start)

    class Meta:
        ordering = ["name"]
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
