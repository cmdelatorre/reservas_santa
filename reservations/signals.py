from django.conf import settings
from django.core.mail import mail_admins
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

    mail_admins("Notificación de reserva", msg, fail_silently=settings.DEBUG)
