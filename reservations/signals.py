from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Reservation


@receiver(pre_save, sender=Reservation)
def validate_reservation(sender, instance, raw, using, update_fields, **kwargs):

    print("saved", instance)
