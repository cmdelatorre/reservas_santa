from datetime import date, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from itertools import islice

from reservations.turns import resolve_turns_in_order_for_year, compute_turns


User = get_user_model()


class ResolveTurnsInOrderForYearTestCase(TestCase):
    def test_round_robin(self):
        turns_2020 = resolve_turns_in_order_for_year(2020)
        turns_2021 = resolve_turns_in_order_for_year(2021)
        self.assertEqual(turns_2021[0], turns_2020[-1])  # Last becomes first
        self.assertListEqual(turns_2021[1:], turns_2020[0:-1])  # Rest is equal

    def test_after_eight_years_starts_again(self):
        self.assertListEqual(
            resolve_turns_in_order_for_year(2020), resolve_turns_in_order_for_year(2027)
        )


class ComputeTurnsTestCase(TestCase):
    def setUp(self):
        # Create test users as turn responsibles
        for name in settings.TURN_RESPONSIBLES:
            User.objects.create(email=f"{name}@example.com")

        self.test_first_day = date(2021, 1, 1)
        self.test_len = 10  # whatever
        self.test_turns = compute_turns(
            year=2021, date_start=self.test_first_day, turn_length=self.test_len
        )

    def test_creates_all_turns_of_equal_size(self):
        for _, t in self.test_turns.items():
            turn_len = (t.to_date - t.from_date).days + 1  # Last day is included
            self.assertEqual(turn_len, self.test_len)

    def test_each_turn_starts_day_after_other_turn_ends(self):
        turns = self.test_turns.values()
        # Iterate pairs (current, next): https://stackoverflow.com/a/5434929/1161156
        for current_turn, next_turn in zip(turns, islice(turns, 1, None)):
            self.assertEqual(
                next_turn.from_date, current_turn.to_date + timedelta(days=1)
            )

    def test_first_turn_is_correct(self):
        fst_turn = list(self.test_turns.values())[0]
        self.assertEqual(fst_turn.from_date, self.test_first_day)
