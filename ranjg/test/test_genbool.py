import unittest
from unittest import mock

from ranjg import genbool, Options
from .._context import Context
from ..factory import BoolGenerator


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
        _options_dummy = Options.default()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "boolean"}, None, False, None),
            ({"type": "boolean"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with mock.patch('ranjg.factory.BoolGenerator.gen') as mock_gen:
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

    def test_gen_with_option_default_prob_of_true_given_bool(self):
        """ Normalized System Test

        ``BoolGenerator#gen(schema)`` uses a option ``default_prob_of_true_given_bool`` (float, 0.0 <= x <= 1.0).

        If ``default_prob_of_true_given_bool`` x is specified, returns True with probability x, False with probability
        1-x.

        assert that:
            When ``default_prob_of_true_given_bool`` is 1.0 (or 0.0), returns True (False).
        """
        options_0 = Options(default_prob_of_true_given_bool=0.0)
        options_1 = Options(default_prob_of_true_given_bool=1.0)
        schema = {'type': 'boolean'}

        # x = 0.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = BoolGenerator().gen(schema, options=options_0)

            assert generated is False

        # x = 1.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = BoolGenerator().gen(schema, options=options_1)

            assert generated is True
