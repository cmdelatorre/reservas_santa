from datetime import timedelta
from django.conf import settings

from reservations.models import Reservation


TURN_DEFAULT_NOTE_TEMPLATE = "Turno de verano de {}"

# The following function must be revised if the TURN_RESPONSIBLES change in any way!
def resolve_turns_in_order_for_year(year):
    """Turns shift in a round-robin. """
    people = list(settings.TURN_RESPONSIBLES.keys())
    N = len(people)
    cut = N - (year - settings.INITIAL_YEAR_COUNT) % N
    return people[cut:] + people[:cut]


def compute_turns(year=None, date_start=None, turn_length=None):
    # períodos = ...
    # responsibles_order = ...  # definir el orden de los responsables para el año en curso
    # reservations = compute_turn_reservations()
    from django.contrib.auth import get_user_model

    turns = {}
    turn_initial_date = date_start
    for turn_name in resolve_turns_in_order_for_year(year):
        turn_final_date = turn_initial_date + timedelta(days=turn_length - 1)
        reservation = Reservation(
            from_date=turn_initial_date,
            to_date=turn_final_date,
            user=get_user_model().objects.get(pk=settings.TURN_RESPONSIBLES[turn_name]),
            notes=TURN_DEFAULT_NOTE_TEMPLATE.format(turn_name),
        )
        turns[turn_name] = reservation
        turn_initial_date = turn_final_date + timedelta(
            days=1
        )  # The next turn starts the next day

    return turns
