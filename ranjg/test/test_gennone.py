import unittest
from unittest import mock

from ranjg import gennone, Options
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
        _options_dummy = Options()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "null"}, None, False, None),
            ({"type": "null"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with mock.patch('ranjg._generator.NoneGenerator.gen') as mock_gen:
                gennone(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(schema, context=context, schema_is_validated=is_validated,
                                                 options=options)


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
