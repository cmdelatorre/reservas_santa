import logging

from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

from reservations.models import Reservation


logger = logging.getLogger(__name__)


TURN_DEFAULT_NOTE_TEMPLATE = "Turno de verano {} de {}"

# The following function must be revised if the TURN_RESPONSIBLES change in any way!
def resolve_turns_in_order_for_year(year):
    """Turns shift in a round-robin. Compute the turns order for the given year."""

    people = list(settings.TURN_RESPONSIBLES.keys())
    N = len(people)
    cut = N - (year - settings.INITIAL_YEAR_COUNT) % N
    return people[cut:] + people[:cut]


def compute_turns(year=None, date_start=None, turn_length=None):
    """Build the Reservation objects (don't save) corresponding to the summer turns for the given
    year.

    Args:
        year (int): [description]. Defaults to None.
        date_start (datetime.date): [description]. Defaults to None.
        turn_length (int): [description]. Defaults to None.

    Returns:
        dict (ordered): A Reservation object for each turn. Keys are turn names.
    """
    turns = {}
    turn_initial_date = date_start
    for turn_name in resolve_turns_in_order_for_year(year):
        turn_final_date = turn_initial_date + timedelta(days=turn_length - 1)
        user_id = settings.TURN_RESPONSIBLES[turn_name]
        logger.info(f"Preparing turn configuration for {turn_name} ({user_id})")
        reservation = Reservation(
            from_date=turn_initial_date,
            to_date=turn_final_date,
            user=get_user_model().objects.get(pk=user_id),
            notes=TURN_DEFAULT_NOTE_TEMPLATE.format(year, turn_name),
        )
        turns[turn_name] = reservation
        turn_initial_date = turn_final_date + timedelta(
            days=1
        )  # The next turn starts the next day

    return turns
