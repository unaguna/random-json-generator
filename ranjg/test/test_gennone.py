import unittest
from unittest import mock

from ranjg import gennone
from .._context import Context
from .._generator import NoneGenerator


class TestGennone(unittest.TestCase):
    """Test class of ``gennone``

    Test ``ranjg.gennone``
    """

    def test_gennone(self):
        """ Normalized System Test

        ``gennone()`` is wrapper of ``NoneGenerator#gen()``.

        assert that:
            When ``gennone`` is called, then ``NoneGenerator#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        params_list = (
            (None, None, False),
            ({"type": "null"}, None, False),
            ({"type": "null"}, None, True),
            (None, _context_dummy, False),
        )

        for schema, context, is_validated in params_list:
            with mock.patch('ranjg._generator.NoneGenerator.gen') as mock_gen:
                gennone(schema, context=context, schema_is_validated=is_validated)
                mock_gen.assert_called_once_with(schema, context=context, schema_is_validated=is_validated)


class TestNoneGenerator(unittest.TestCase):
    """Test class of ``NoneGenerator``

    Test ``NoneGenerator``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``NoneGenerator().gen(schema)`` returns ``None``. It does nothing else.

        assert that:
            ``NoneGenerator().gen(schema)`` returns ``None``.
        """
        self.assertIsNone(NoneGenerator().gen({}))
