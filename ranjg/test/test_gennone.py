import unittest
from unittest import mock

from ranjg import gennone, Options
from .._context import Context
from ..factory import NoneFactory


class TestGennone(unittest.TestCase):
    """Test class of ``gennone``

    Test ``ranjg.gennone``
    """

    def test_gennone(self):
        """ Normalized System Test

        ``gennone()`` is wrapper of ``NoneFactory#gen()``.

        assert that:
            When ``gennone`` is called, then ``NoneFactory#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        _options_dummy = Options.default()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "null"}, None, False, None),
            ({"type": "null"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with self.subTest(schema=schema, is_validated=is_validated, options=(options is not None)), \
                    mock.patch('ranjg.factory.NoneFactory.gen') as mock_gen:
                gennone(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(context=context, options=options)
            # TODO: schema, schema_is_validated についても assert する


class TestNoneFactory(unittest.TestCase):
    """Test class of ``NoneFactory``

    Test ``NoneFactory``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``NoneFactory(schema).gen()`` returns ``None``. It does nothing else.

        assert that:
            ``NoneFactory(schema).gen()`` returns ``None``.
        """
        self.assertIsNone(NoneFactory({}).gen())
