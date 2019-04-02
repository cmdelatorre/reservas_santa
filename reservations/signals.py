from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from reservations.models import Reservation


new_reservation_prefix = "Nueva reserva:"
reservation_edit_prefix = "Una reserva a sido editada:"

message_template = """
    Quién: {user} <{r.user.email}>
    Desde: {r.from_date}
    Hasta: {r.to_date}
    Habitaciones: {r.rooms_str}
    Notas: {r.notes}

Ver en Santa Reserva: {link}

"""


@receiver(
    post_save, sender=Reservation, dispatch_uid="send_email_notifying_reservation"
)
def send_email_notifying_reservation(sender, instance, created, **kwargs):
    prefix = reservation_edit_prefix
    if created:
        prefix = new_reservation_prefix

    url = "https://santa-reserva.herokuapp.com{}".format(instance.get_absolute_url())
    msg = (prefix + message_template).format(
        r=instance, user=instance.user.get_full_name(), link=url
    )

    send_mail(
        "Notificación de reserva",
        msg,
        settings.SERVER_EMAIL,
        [u.email for u in get_user_model().objects.filter(is_superuser=True)],
        fail_silently=not settings.DEBUG,
    )
