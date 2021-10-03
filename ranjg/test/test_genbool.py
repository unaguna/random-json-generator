import unittest

from ranjg import Options
from ..factories import BoolFactory


class TestBoolFactory(unittest.TestCase):
    """Test class of ``BoolFactory``

    Test ``BoolFactory``
    """

    def test_gen(self):
        """ Normalized System Test

        ``BoolFactory#gen()`` returns ``True`` or ``False`` randomly.

        assert that:
            ``BoolFactory#gen()`` returns boolean value.
        """
        self.assertIsInstance(BoolFactory({}).gen(), bool)

    def test_gen_with_option_default_prob_of_true_given_bool(self):
        """ Normalized System Test

        ``BoolFactory#gen(schema)`` uses a option ``default_prob_of_true_given_bool`` (float, 0.0 <= x <= 1.0).

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
            generated = BoolFactory(schema).gen(options=options_0)

            assert generated is False

        # x = 1.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = BoolFactory(schema).gen(options=options_1)

            assert generated is True
