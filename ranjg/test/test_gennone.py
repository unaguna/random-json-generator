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
            (None, {}, None, None),
            ({"type": "null"}, {"type": "null"}, None, None),
            (None, {}, _context_dummy, _context_dummy),
        )

        for schema_arg, schema_used, context_arg, context_used in params_list:
            with mock.patch('ranjg._generator.NoneGenerator.gen') as mock_gen:
                gennone(schema_arg, context=context_arg)
                mock_gen.assert_called_once_with(schema_used, context=context_used)


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
