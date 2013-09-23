from django_utils.decorators.profiling import trace
from sys import exc_info
from traceback import extract_tb
from unittest import TestCase


class Profiling(TestCase):
    def test_nested_function_has_valid_traceback(self):
        with self.assertRaises(Exception) as context:
            @trace
            def nested_function_one():
                def nested_function_two():
                    def nested_function_three():
                        raise Exception('Test exception')

                    nested_function_three()

                nested_function_two()

            nested_function_one()

        self.assertEqual(context.exception.message, 'Test exception')

        exc_type, exc_value, exc_traceback = exc_info()
        has_inner_exception = False

        for line in extract_tb(exc_traceback):
            if 'nested_function_three' in line[3]:
                has_inner_exception = True
                break

        message = 'nested_function_three() is not referenced in traceback'
        self.assertTrue(has_inner_exception, message)
