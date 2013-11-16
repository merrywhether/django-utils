import unittest
# import django_utils

from django_utils.management.commands.notifier import slack


class NotifierTests(unittest.TestCase):
    def test_slask(self):
        is_valid = slack('#kojak', 'Test the rocket.')
        self.assertTrue(is_valid)
