import unittest
from unittest import mock

from ranjg import genbool
from .._context import Context
from .._generator import BoolGenerator


class TestGenbool(unittest.TestCase):
    """Test class of ``genbool``

    Test ``ranjg.genbool``
    """

    def test_genbool(self):
        """ Normalized System Test

        ``genbool()`` is wrapper of ``BoolGenerator#gen()``.

        assert that:
            When ``genbool`` is called, then ``BoolGenerator#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        params_list = (
            (None, {}, None, None),
            ({"type": "boolean"}, {"type": "boolean"}, None, None),
            (None, {}, _context_dummy, _context_dummy),
        )

        for schema_arg, schema_used, context_arg, context_used in params_list:
            with mock.patch('ranjg._generator.BoolGenerator.gen') as mock_gen:
                genbool(schema_arg, context=context_arg)
                mock_gen.assert_called_once_with(schema_used, context=context_used)


class TestBoolGenerator(unittest.TestCase):
    """Test class of ``BoolGenerator``

    Test ``BoolGenerator``
    """

    def test_gen(self):
        """ Normalized System Test

        ``BoolGenerator#gen()`` returns ``True`` or ``False`` randomly.

        assert that:
            ``BoolGenerator#gen()`` returns boolean value.
        """
        self.assertIsInstance(BoolGenerator().gen({}), bool)
