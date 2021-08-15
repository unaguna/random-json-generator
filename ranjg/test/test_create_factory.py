import unittest

from ranjg.factory.__function import _raffle_type


class TestRaffleType(unittest.TestCase):
    """Test class of ``_raffle_type``

    Test ``ranjg.__gen._raffle_type``
    """

    def test_raffle_type_with_none(self):
        """ Normalized System Test

        If argument ``schema_type`` is None, returns None.

        assert that:
            If ``schema_type`` is None, ``_raffle_type(schema_type)`` returns None.
        """
        choice = _raffle_type(None)
        self.assertIsNone(choice)

    def test_raffle_type_with_str(self):
        """ Normalized System Test

        If argument ``schema_type`` is string, returns it.

        assert that:
            If ``schema_type`` is string, ``_raffle_type(schema_type)`` returns string same to the argument.
        """
        schema_type_list = ("null", "boolean", "integer", "number", "string", "array", "object")

        for schema_type in schema_type_list:
            with self.subTest(type=schema_type):
                choice = _raffle_type(schema_type)
                self.assertEqual(choice, schema_type)

    def test_raffle_type_with_list(self):
        """ Normalized System Test

        If argument ``schema_type`` is non-empty list, returns a string in the argument.

        assert that:
            If ``schema_type`` is non-empty list, ``_raffle_type(schema_type)`` returns a string of the argument.
        """
        schema_type_list = (["null", "boolean", "integer", "number", "string", "array", "object"],
                            ["null", "number"],
                            ["string", "boolean"])

        for schema_type in schema_type_list:
            with self.subTest(type=schema_type):
                for i in range(5):
                    choice = _raffle_type(schema_type)
                    self.assertIn(choice, schema_type)

    def test_raffle_type_with_empty_list(self):
        """ Normalized System Test

        If argument ``schema_type`` is empty list, returns None.

        assert that:
            If ``schema_type`` is empty list, ``_raffle_type(schema_type)`` returns None.
        """
        self.assertRaises(ValueError, lambda: _raffle_type([]))