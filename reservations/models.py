from django.conf import settings
from django.db import models


class Reservation(models.Model):
    from_date = models.DateField("desde")
    to_date = models.DateField("hasta")
    rooms = models.ManyToManyField(
        "rooms.room", verbose_name="Habitación reservada", related_name="reservations"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="persona",
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    notes = models.TextField("notas", blank=True, default="")

    def __str__(self):
        return "{r.id}) Reserva de {r.user} ({r.from_date} al {r.to_date})".format(
            r=self
        )

    @property
    def rooms_str(self):
        return ", ".join(map(str, self.rooms.all()))

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("reservations:edit", args=[str(self.id)])

    class Meta:
        ordering = ["from_date", "to_date"]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
