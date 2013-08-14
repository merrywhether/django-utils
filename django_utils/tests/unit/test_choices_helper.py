from django.test import TestCase
from global_helpers.choices_helper import get_choice_by_id, get_id_by_nice_name
from model_utils import Choices


TEST_CHOICES = Choices(
    (1, 'choice1', ('Choice 1')),
    (2, 'choice2', ('Choice 2')),
)


class ChoicesHelper(TestCase):
    def test_get_choice_by_nice_name(self):
        id = get_id_by_nice_name(TEST_CHOICES, 'Choice 1')
        self.assertTrue(id == 1)

    def test_get_choice_by_id_not_in_index(self):
        c = get_choice_by_id(TEST_CHOICES, 2)
        self.assertTrue(c[0] == 2)
        self.assertTrue(c[1] == 'Choice 2')
