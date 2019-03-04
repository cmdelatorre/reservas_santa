from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=200, verbose_name="nombre de la habitación")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
