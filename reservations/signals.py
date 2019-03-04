from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from reservations.models import Reservation
from rooms.models import Room


@receiver(
    m2m_changed, sender=Reservation.rooms.through, dispatch_uid="my_unique_identifier"
)
def validate_reservation(
    sender, instance, action, reverse, model, pk_set, using, **kwargs
):
    if instance.from_date >= instance.to_date:
        raise Exception("from_date expected earlier than to_date")

    potential_conflicts = Reservation.objects.exclude(id=instance.id).filter(
        to_date__gt=instance.from_date, from_date__lt=instance.to_date
    )

    reserved_rooms_ids = set(potential_conflicts.values_list("rooms__id", flat=True))
    conflicting_rooms = reserved_rooms_ids.intersection(pk_set)

    if conflicting_rooms:
        rooms = [str(r) for r in Room.objects.filter(id__in=conflicting_rooms)]
        msg = "Invalid rooms selection. Rooms already reserved for the period: {}".format(
            rooms
        )
        raise Exception(msg)
