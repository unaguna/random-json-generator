import unittest
from unittest import mock

from ranjg import genbool, Options
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
        _options_dummy = Options()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "boolean"}, None, False, None),
            ({"type": "boolean"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with mock.patch('ranjg._generator.BoolGenerator.gen') as mock_gen:
                genbool(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(schema, context=context, schema_is_validated=is_validated,
                                                 options=options)


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
