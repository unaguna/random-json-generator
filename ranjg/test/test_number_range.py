import itertools
import unittest

from .._number_range import _from_schema, _normalize_minimum, _normalize_maximum


class TestFromSchema(unittest.TestCase):
    """Test class of ``from_schema``

    Test ``ranjg._number_range._from_schema``
    """

    def test_make_range_with_empty_schema(self):
        """ Normalized System Test

        When ``schema`` is empty, both of ``minimum`` and ``maximum`` is not specified. If ``minimum`` is not specified,
        ``exclusive_minimum`` is False. ``maximum`` and ``exclusive_maximum`` are same to them.

        assert that:
            When the schema is empty, ``minimum`` and ``maximum`` is None and ``exclusive_minimum`` and
            ``exclusive_maximum`` are False.
        """
        schema = {}
        number_range = _from_schema(schema)
        self.assertIsNone(number_range.minimum)
        self.assertIsNone(number_range.maximum)
        self.assertFalse(number_range.exclusive_minimum)
        self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_schema(self):
        """ Normalized System Test

        Detailed testing is done on the tests of ``_normalize_minimum`` and ``_normalize_maximum``.
        """
        param_list = ((5.1, None, 6.5, None, 5.1, False, 6.5, False),
                      (5.1, True, 6.5, None, 5.1, True, 6.5, False),
                      (5.1, None, 6.5, True, 5.1, False, 6.5, True),
                      (5.1, 5.3, 6.5, 6.7, 5.3, True, 6.5, False))

        for minimum, ex_min, maximum, ex_max, expected_min, expected_ex_min, expected_max, expected_ex_max \
                in param_list:
            with self.subTest(minimum=minimum, ex_min=ex_min, maximum=maximum, ex_max=ex_max):
                schema = {
                    "minimum": minimum,
                    "exclusiveMinimum": ex_min,
                    "maximum": maximum,
                    "exclusiveMaximum": ex_max,
                }
            number_range = _from_schema(schema)
            self.assertEqual(number_range.minimum, expected_min)
            self.assertEqual(number_range.maximum, expected_max)
            self.assertEqual(number_range.exclusive_minimum, expected_ex_min)
            self.assertEqual(number_range.exclusive_maximum, expected_ex_max)


class TestNormalizeMinimum(unittest.TestCase):
    """Test class of ``_normalize_minimum``

    Test ``ranjg._number_range._normalize_minimum``
    """

    def test_normalize_min_with_no_args(self):
        """ Normalized System Test

        When conditions are not specified, the result ``minimum`` is None and the result ``exclusive_minimum`` is False.
        ``minimum is None`` means that the lower bound is -inf. In this case, ``exclusive_minimum`` is defined as False.

        assert that:
            When the arguments are None, ``minimum`` is None and ``exclusive_minimum`` is False.
        """
        generated_minimum, generated_ex_min = _normalize_minimum(minimum=None,
                                                                 exclusive_minimum=None)
        self.assertIsNone(generated_minimum)
        self.assertFalse(generated_ex_min)

    def test_normalize_min_with_min(self):
        """ Normalized System Test

        When argument ``minimum`` is specified and argument ``exclusive_minimum`` is not specified, the ``minimum`` of
        result equals to the argument ``minimum`` and ``exclusive_minimum`` is False.

        assert that:
            When only ``minimum`` is specified, the ``minimum`` of result equals to the argument ``minimum`` and
            ``exclusive_minimum`` is False.
        """
        minimum_list = (-3, 0.0, 2.2)

        for minimum in minimum_list:
            with self.subTest(minimum=minimum):
                generated_minimum, generated_ex_min = _normalize_minimum(minimum=minimum,
                                                                         exclusive_minimum=None)
                self.assertEqual(generated_minimum, minimum)
                self.assertFalse(generated_ex_min)

    def test_normalize_min_with_exMin_bool(self):
        """ Normalized System Test

        When argument ``exclusiveMinimum`` is specified with boolean value and ``minimum`` is not specified, they
        are ignored. In other words, normalization acts similarly if its arguments are not specified.

        assert that:
             When argument ``exclusiveMinimum`` is specified with boolean value and ``minimum`` is not specified,
             result ``minimum`` is None and ``exclusive_minimum`` is False.
        """
        exclusive_minimum_list = (True, False)

        for exclusive_minimum in exclusive_minimum_list:
            with self.subTest(ex_min=exclusive_minimum):
                generated_minimum, generated_ex_min = _normalize_minimum(minimum=None,
                                                                         exclusive_minimum=exclusive_minimum)
                self.assertIsNone(generated_minimum)
                self.assertFalse(generated_ex_min)

    def test_normalize_min_with_min_exMin_bool(self):
        """ Normalized System Test

        When argument ``minimum`` is specified and argument ``exclusive_minimum`` is boolean value, the ``minimum`` of
        the result equals to the argument ``minimum`` and ``exclusive_minimum`` of the result equals to the argument
        ``exclusive_minimum``.

        assert that:
            When ``minimum`` is specified and argument ``exclusive_minimum`` is boolean value, the ``minimum`` of
            result equals to the argument ``minimum`` and ``exclusive_minimum`` of the result equals to the argument
            ``exclusive_minimum``.
        """
        minimum_list = (-3, 0.0, 2.2)
        exclusive_minimum_list = (True, False)

        for minimum, exclusive_minimum in itertools.product(minimum_list, exclusive_minimum_list):
            with self.subTest(minimum=minimum, ex_min=exclusive_minimum):
                generated_minimum, generated_ex_min = _normalize_minimum(minimum=minimum,
                                                                         exclusive_minimum=exclusive_minimum)
                self.assertEqual(generated_minimum, minimum)
                self.assertEqual(generated_ex_min, exclusive_minimum)

    def test_normalize_min_with_exMin_number(self):
        """ Normalized System Test

        When argument ``minimum`` is not specified and argument ``exclusive_minimum`` is number, the ``minimum`` of
        result equals to the argument ``exclusive_minimum`` and ``exclusive_minimum`` of result is True.

        assert that:
            When only ``schema.exclusiveMinimum`` is specified and it is number, the ``minimum`` of result equals to
            argument ``exclusiveMinimum`` and ``exclusive_minimum`` of result is True.
        """
        minimum_list = (-3, 0.0, 2.2)

        for exclusive_minimum in minimum_list:
            with self.subTest(ex_min=exclusive_minimum):
                generated_minimum, generated_ex_min = _normalize_minimum(minimum=None,
                                                                         exclusive_minimum=exclusive_minimum)
                self.assertEqual(generated_minimum, exclusive_minimum)
                self.assertTrue(generated_ex_min)

    def test_normalize_min_with_min_exMin_number(self):
        """ Normalized System Test

        When arguments ``minimum`` and ``exclusiveMinimum`` are specified with number, the stricter one applies.

        assert that:
            When the arguments specify ``minimum > exclusiveMinimum``, the ``minimum`` of result equals to argument
            ``minimum`` and ``exclusive_minimum`` of result is False.
            When the arguments specify ``minimum <= exclusiveMinimum``, the ``minimum`` of result equals to argument
            ``exclusiveMinimum`` and ``exclusive_minimum`` of result is True.
        """
        param_list = ((-2.0, -2.0, -2.0, True),
                      (-2.0, -1.9, -1.9, True),
                      (-1.9, -2.0, -1.9, False),
                      (0, 0, 0, True),
                      (0, .1, .1, True),
                      (.1, 0, .1, False))

        for minimum, exclusive_minimum, expected_minimum, expected_exclusive_minimum in param_list:
            with self.subTest(minimum=minimum, ex_min=exclusive_minimum):
                generated_minimum, generated_ex_min = _normalize_minimum(minimum=minimum,
                                                                         exclusive_minimum=exclusive_minimum)
                self.assertEqual(generated_minimum, expected_minimum)
                self.assertEqual(generated_ex_min, expected_exclusive_minimum)


class TestNormalizeMaximum(unittest.TestCase):
    """Test class of ``_normalize_maximum``

    Test ``ranjg._number_range._normalize_maximum``
    """

    def test_normalize_max_with_no_args(self):
        """ Normalized System Test

        When conditions are not specified, the result ``maximum`` is None and the result ``exclusive_maximum`` is False.
        ``maximum is None`` means that the lower bound is -inf. In this case, ``exclusive_maximum`` is defined as False.

        assert that:
            When the arguments are None, ``maximum`` is None and ``exclusive_maximum`` is False.
        """
        generated_maximum, generated_ex_max = _normalize_maximum(maximum=None,
                                                                 exclusive_maximum=None)
        self.assertIsNone(generated_maximum)
        self.assertFalse(generated_ex_max)

    def test_normalize_max_with_max(self):
        """ Normalized System Test

        When argument ``maximum`` is specified and argument ``exclusive_maximum`` is not specified, the ``maximum`` of
        result equals to the argument ``maximum`` and ``exclusive_maximum`` is False.

        assert that:
            When only ``maximum`` is specified, the ``maximum`` of result equals to the argument ``maximum`` and
            ``exclusive_maximum`` is False.
        """
        maximum_list = (-3, 0.0, 2.2)

        for maximum in maximum_list:
            with self.subTest(maximum=maximum):
                generated_maximum, generated_ex_max = _normalize_maximum(maximum=maximum,
                                                                         exclusive_maximum=None)
                self.assertEqual(generated_maximum, maximum)
                self.assertFalse(generated_ex_max)

    def test_normalize_max_with_exMax_bool(self):
        """ Normalized System Test

        When argument ``exclusiveMaximum`` is specified with boolean value and ``maximum`` is not specified, they
        are ignored. In other words, normalization acts similarly if its arguments are not specified.

        assert that:
             When argument ``exclusiveMaximum`` is specified with boolean value and ``maximum`` is not specified,
             result ``maximum`` is None and ``exclusive_maximum`` is False.
        """
        exclusive_maximum_list = (True, False)

        for exclusive_maximum in exclusive_maximum_list:
            with self.subTest(ex_max=exclusive_maximum):
                generated_maximum, generated_ex_max = _normalize_maximum(maximum=None,
                                                                         exclusive_maximum=exclusive_maximum)
                self.assertIsNone(generated_maximum)
                self.assertFalse(generated_ex_max)

    def test_normalize_max_with_max_exMax_bool(self):
        """ Normalized System Test

        When argument ``maximum`` is specified and argument ``exclusive_maximum`` is boolean value, the ``maximum`` of
        the result equals to the argument ``maximum`` and ``exclusive_maximum`` of the result equals to the argument
        ``exclusive_maximum``.

        assert that:
            When ``maximum`` is specified and argument ``exclusive_maximum`` is boolean value, the ``maximum`` of
            result equals to the argument ``maximum`` and ``exclusive_maximum`` of the result equals to the argument
            ``exclusive_maximum``.
        """
        maximum_list = (-3, 0.0, 2.2)
        exclusive_maximum_list = (True, False)

        for maximum, exclusive_maximum in itertools.product(maximum_list, exclusive_maximum_list):
            with self.subTest(maximum=maximum, ex_max=exclusive_maximum):
                generated_maximum, generated_ex_max = _normalize_maximum(maximum=maximum,
                                                                         exclusive_maximum=exclusive_maximum)
                self.assertEqual(generated_maximum, maximum)
                self.assertEqual(generated_ex_max, exclusive_maximum)

    def test_normalize_max_with_exMax_number(self):
        """ Normalized System Test

        When argument ``maximum`` is not specified and argument ``exclusive_maximum`` is number, the ``maximum`` of
        result equals to the argument ``exclusive_maximum`` and ``exclusive_maximum`` of result is True.

        assert that:
            When only ``schema.exclusiveMaximum`` is specified and it is number, the ``maximum`` of result equals to
            argument ``exclusiveMaximum`` and ``exclusive_maximum`` of result is True.
        """
        maximum_list = (-3, 0.0, 2.2)

        for exclusive_maximum in maximum_list:
            with self.subTest(ex_max=exclusive_maximum):
                generated_maximum, generated_ex_max = _normalize_maximum(maximum=None,
                                                                         exclusive_maximum=exclusive_maximum)
                self.assertEqual(generated_maximum, exclusive_maximum)
                self.assertTrue(generated_ex_max)

    def test_normalize_max_with_max_exMax_number(self):
        """ Normalized System Test

        When arguments ``maximum`` and ``exclusiveMaximum`` are specified with number, the stricter one applies.

        assert that:
            When the arguments specify ``maximum > exclusiveMaximum``, the ``maximum`` of result equals to argument
            ``maximum`` and ``exclusive_maximum`` of result is False.
            When the arguments specify ``maximum <= exclusiveMaximum``, the ``maximum`` of result equals to argument
            ``exclusiveMaximum`` and ``exclusive_maximum`` of result is True.
        """
        param_list = ((-2.0, -2.0, -2.0, True),
                      (-2.0, -2.1, -2.1, True),
                      (-2.1, -2.0, -2.1, False),
                      (0, 0, 0, True),
                      (0, -.1, -.1, True),
                      (-.1, 0, -.1, False))

        for maximum, exclusive_maximum, expected_maximum, expected_exclusive_maximum in param_list:
            with self.subTest(maximum=maximum, ex_max=exclusive_maximum):
                generated_maximum, generated_ex_max = _normalize_maximum(maximum=maximum,
                                                                         exclusive_maximum=exclusive_maximum)
                self.assertEqual(generated_maximum, expected_maximum)
                self.assertEqual(generated_ex_max, expected_exclusive_maximum)
