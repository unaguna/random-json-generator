import itertools
import unittest
import jsonschema
from ranjg import gennum
from ..__gennum import NumberRange
from ranjg.error import SchemaConflictError


class TestGennum(unittest.TestCase):
    """Test class of ``gennum``

    Test ``ranjg.gennum``
    """

    def test_gennum_with_empty_schema(self):
        """ Normalized System Test

        ``gennum(schema)`` returns a number value even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``gennum(schema)`` returns ``float`` value.
        """
        schema = {}

        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        jsonschema.validate(generated, schema)

    def test_gennum_with_param_minimum(self):
        """ Normalized System Test

        When ``properties.minimum`` is specified, the result number ``x`` satisfies `` x >= minimum``.

        assert that:
            When the schema has ``minimum``, ``gennum(schema)`` returns ``float`` value ``x`` and it satisfies
            `` x >= minimum``.
        """
        threshold_list = (-1.4, 0, 1.23)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "minimum": threshold,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertGreaterEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_maximum(self):
        """ Normalized System Test

        When ``properties.maximum`` is specified, the result number ``x`` satisfies `` x <= maximum``.

        assert that:
            When the schema has ``maximum``, ``gennum(schema)`` returns ``float`` value ``x`` and it satisfies
            `` x <= maximum``.
        """
        threshold_list = (-1.4, 0, 1.23)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "maximum": threshold,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertLessEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_exclusiveMinimum(self):
        """ Normalized System Test

        When ``properties.exclusiveMinimum`` is specified by a number, the result number ``x`` satisfies
        `` x > exclusiveMinimum``.

        assert that:
            When the schema has ``properties.exclusiveMinimum`` as number, ``gennum(schema)`` returns ``float`` value
            ``x`` and it satisfies `` x > exclusiveMinimum``.
        """
        threshold_list = (-1.4, 0, 1.23)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "exclusiveMinimum": threshold,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertGreater(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_exclusiveMaximum(self):
        """ Normalized System Test

        When ``properties.exclusiveMaximum`` is specified by a number, the result number ``x`` satisfies
        `` x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.exclusiveMaximum`` as number, ``gennum(schema)`` returns ``float`` value
            ``x`` and it satisfies `` x < exclusiveMaximum``.
        """
        threshold_list = (-1.4, 0, 1.23)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "exclusiveMaximum": threshold,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertLess(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_minimum_exclusiveMinimum(self):
        """ Normalized System Test

        When both ``properties.minimum`` and ``properties.exclusiveMinimum: number`` are specified, the result number
        ``x`` satisfies ``x >= maximum`` and ``x > exclusiveMaximum``.

        assert that:
            When the schema has ``properties.minimum`` and ``properties.exclusiveMinimum`` as number, ``gennum(schema)``
            returns ``float`` value ``x`` and it satisfies ``x >= minimum`` and ``x > exclusiveMinimum``.
        """
        thresholds_list = ((1.23E+200, 1.23),
                           (1.23, 1.23E+200))
        for minimum, exclusive_minimum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_minimum=exclusive_minimum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMinimum": exclusive_minimum,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertGreaterEqual(generated, minimum)
                self.assertGreater(generated, exclusive_minimum)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_maximum_exclusiveMaximum(self):
        """ Normalized System Test

        When both ``properties.maximum`` and ``properties.exclusiveMaximum: number`` are specified, the result number
        ``x`` satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.maximum`` and ``properties.exclusiveMaximum`` as number, ``gennum(schema)``
            returns ``float`` value ``x`` and it satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.
        """
        thresholds_list = ((1.23E+200, 1.23),
                           (1.23, 1.23E+200))
        for maximum, exclusive_maximum in thresholds_list:
            with self.subTest(maximum=maximum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "maximum": maximum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertLessEqual(generated, maximum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_minimum_maximum(self):
        """ Normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``minimum <= x <= maximum``.

        assert that:
            When the schema has ``properties.minimum`` and ``properties.maximum`, ``gennum(schema)`` returns ``float``
            value ``x`` and it satisfies ``minimum <= x <= maximum``.
        """
        thresholds_list = ((-1.5, -1.2),
                           (-1.2, -1.2),
                           (-1.5, 0),
                           (-1.5, 1.2),
                           (0, 0),
                           (0, 1.2),
                           (1.1, 1.2),
                           (1.2, 1.2))
        for minimum, maximum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                }
                generated = gennum(schema)
                self.assertIsInstance(generated, float)
                self.assertGreaterEqual(generated, minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_gennum_with_param_conflict_minimum_maximum(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``minimum <= x <= maximum``. As a result, when ``maximum < minimum``, SchemaConflictError is
        raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum`, ``gennum(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((-1.5, -1.2),
                           (-1.5, 0),
                           (-1.5, 1.2),
                           (0, 1.2),
                           (1.1, 1.2))
        for maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: gennum(schema))

    def test_gennum_with_param_conflict_exclusive_minimum_maximum(self):
        """ Semi-normalized System Test

        When both ``properties.exclusive_minimum: number`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``exclusive_minimum < x <= maximum``. As a result, when ``maximum <= exclusive_minimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.maximum <= properties.exclusive_minimum`, ``gennum(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((-1.5, -1.2),
                           (-1.2, -1.2),
                           (-1.5, 0),
                           (-1.5, 1.2),
                           (0, 0),
                           (0, 1.2),
                           (1.1, 1.2),
                           (1.2, 1.2))
        for maximum, exclusive_minimum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, maximum=maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "maximum": maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: gennum(schema))

    def test_gennum_with_param_conflict_minimum_exclusive_maximum(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.exclusive_maximum: number`` are specified, the result number
        ``x`` satisfies ``minimum <= x < exclusive_maximum``. As a result, when ``exclusive_maximum <= minimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.exclusive_maximum <= properties.minimum`, ``gennum(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((-1.5, -1.2),
                           (-1.2, -1.2),
                           (-1.5, 0),
                           (-1.5, 1.2),
                           (0, 0),
                           (0, 1.2),
                           (1.1, 1.2),
                           (1.2, 1.2))
        for exclusive_maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: gennum(schema))

    def test_gennum_with_param_conflict_exclusive_minimum_exclusive_maximum(self):
        """ Semi-normalized System Test

        When both ``properties.exclusive_minimum: number`` and ``properties.exclusive_maximum: number`` are specified,
        the result number ``x`` satisfies ``exclusive_minimum < x < exclusive_maximum``. As a result, when
        ``exclusive_maximum <= exclusive_minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.exclusive_minimum >= properties.exclusive_maximum`, ``gennum(schema)``
            raised SchemaConflictError.
        """
        thresholds_list = ((-1.5, -1.2),
                           (-1.2, -1.2),
                           (-1.5, 0),
                           (-1.5, 1.2),
                           (0, 0),
                           (0, 1.2),
                           (1.1, 1.2),
                           (1.2, 1.2))
        for exclusive_maximum, exclusive_minimum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: gennum(schema))


class TestGennumRangeFromSchema(unittest.TestCase):
    """Test class of ``NumberRange.from_schema``

    Test ``ranjg.__gennum.NumberRange.from_schema``
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
        number_range = NumberRange.from_schema(schema)
        self.assertIsNone(number_range.minimum)
        self.assertIsNone(number_range.maximum)
        self.assertFalse(number_range.exclusive_minimum)
        self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_min(self):
        """ Normalized System Test

        When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is not specified, the ``minimum`` of result
        equals to ``schema.minimum`` and ``exclusive_minimum`` is False.

        assert that:
            When only ``schema.minimum`` is specified, the ``minimum`` of result equals to ``schema.minimum`` and
            ``exclusive_minimum`` is False.
        """
        minimum_list = (-3, 0.0, 2.2)

        for minimum in minimum_list:
            with self.subTest(minimum=minimum):
                schema = {
                    "minimum": minimum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertEqual(number_range.minimum, minimum)
                self.assertIsNone(number_range.maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_exMin_bool(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` is specified with boolean value and ``schema.minimum`` is not specified, they
        are ignored.

        assert that:
            When ``schema.exclusiveMinimum`` is boolean value and ``schema.minimum`` is not specified, ``minimum`` and
            ``maximum`` is None and ``exclusive_minimum`` and ``exclusive_maximum`` are False.
        """
        exclusive_minimum_list = (True, False)

        for exclusive_minimum in exclusive_minimum_list:
            with self.subTest(ex_min=exclusive_minimum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertIsNone(number_range.minimum)
                self.assertIsNone(number_range.maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_min_exMin_bool(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.exclusiveMinimum`` are specified, the ``minimum`` of result
        equals to ``schema.minimum`` and ``exclusive_minimum`` equals to ``schema.exclusiveMinimum``.

        assert that:
            When ``schema.minimum`` and ``schema.exclusiveMinimum`` is specified, the ``minimum`` of result equals to
            ``schema.minimum`` and the ``exclusive_minimum`` equals to ``schema.exclusiveMinimum``.
        """
        minimum_list = (-3, 0.0, 2.2)
        exclusive_minimum_list = (True, False)

        for minimum, exclusive_minimum in itertools.product(minimum_list, exclusive_minimum_list):
            with self.subTest(minimum=minimum, ex_min=exclusive_minimum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMinimum": exclusive_minimum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertEqual(number_range.minimum, minimum)
                self.assertIsNone(number_range.maximum)
                self.assertEqual(number_range.exclusive_minimum, exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_exMin_number(self):
        """ Normalized System Test

        When ``schema.minimum`` is not specified and ``schema.exclusiveMinimum`` is specified with number, the
        ``minimum`` of result equals to ``schema.exclusiveMinimum`` and ``exclusive_minimum`` is True.

        assert that:
            When only ``schema.exclusiveMinimum`` is specified and it is number, the ``minimum`` of result equals to
            ``schema.exclusiveMinimum`` and ``exclusive_minimum`` is True.
        """
        minimum_list = (-3, 0.0, 2.2)

        for exclusive_minimum in minimum_list:
            with self.subTest(ex_min=exclusive_minimum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertEqual(number_range.minimum, exclusive_minimum)
                self.assertIsNone(number_range.maximum)
                self.assertTrue(number_range.exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_min_exMin_number(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.exclusiveMinimum`` are specified with number, the stricter one applies.

        assert that:
            When only ``schema.minimum > schema.exclusiveMinimum``, the ``minimum`` of result equals to
            ``schema.minimum`` and ``exclusive_minimum`` is False.
            When only ``schema.minimum <= schema.exclusiveMinimum``, the ``minimum`` of result equals to
            ``schema.exclusiveMinimum`` and ``exclusive_minimum`` is True.
        """
        param_list = ((-2.0, -2.0, -2.0, True),
                      (-2.0, -1.9, -1.9, True),
                      (-1.9, -2.0, -1.9, False),
                      (0, 0, 0, True),
                      (0, .1, .1, True),
                      (.1, 0, .1, False))

        for minimum, exclusive_minimum, expected_minimum, expected_exclusive_minimum in param_list:
            with self.subTest(minimum=minimum, ex_min=exclusive_minimum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMinimum": exclusive_minimum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertEqual(number_range.minimum, expected_minimum)
                self.assertIsNone(number_range.maximum)
                self.assertEqual(number_range.exclusive_minimum, expected_exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_max(self):
        """ Normalized System Test

        When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is not specified, the ``maximum`` of result
        equals to ``schema.maximum`` and ``exclusive_maximum`` is False.

        assert that:
            When only ``schema.maximum`` is specified, the ``maximum`` of result equals to ``schema.maximum`` and
            ``exclusive_maximum`` is False.
        """
        maximum_list = (-3, 0.0, 2.2)

        for maximum in maximum_list:
            with self.subTest(maximum=maximum):
                schema = {
                    "maximum": maximum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertIsNone(number_range.minimum)
                self.assertEqual(number_range.maximum, maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_exMax_bool(self):
        """ Normalized System Test

        When ``schema.exclusiveMaximum`` is specified with boolean value and ``schema.maximum`` is not specified, they
        are ignored.

        assert that:
            When ``schema.exclusiveMaximum`` is boolean value and ``schema.maximum`` is not specified, ``maximum`` and
            ``maximum`` is None and ``exclusive_maximum`` and ``exclusive_maximum`` are False.
        """
        exclusive_maximum_list = (True, False)

        for exclusive_maximum in exclusive_maximum_list:
            with self.subTest(ex_max=exclusive_maximum):
                schema = {
                    "exclusiveMaximum": exclusive_maximum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertIsNone(number_range.minimum)
                self.assertIsNone(number_range.maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertFalse(number_range.exclusive_maximum)

    def test_make_range_with_max_exMax_bool(self):
        """ Normalized System Test

        When ``schema.maximum`` and ``schema.exclusiveMaximum`` are specified, the ``maximum`` of result
        equals to ``schema.maximum`` and ``exclusive_maximum`` equals to ``schema.exclusiveMaximum``.

        assert that:
            When ``schema.maximum`` and ``schema.exclusiveMaximum`` is specified, the ``maximum`` of result equals to
            ``schema.maximum`` and the ``exclusive_maximum`` equals to ``schema.exclusiveMaximum``.
        """
        maximum_list = (-3, 0.0, 2.2)
        exclusive_maximum_list = (True, False)

        for maximum, exclusive_maximum in itertools.product(maximum_list, exclusive_maximum_list):
            with self.subTest(maximum=maximum, ex_max=exclusive_maximum):
                schema = {
                    "maximum": maximum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertIsNone(number_range.minimum)
                self.assertEqual(number_range.maximum, maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertEqual(number_range.exclusive_maximum, exclusive_maximum)

    def test_make_range_with_exMax_number(self):
        """ Normalized System Test

        When ``schema.maximum`` is not specified and ``schema.exclusiveMaximum`` is specified with number, the
        ``maximum`` of result equals to ``schema.exclusiveMaximum`` and ``exclusive_maximum`` is True.

        assert that:
            When only ``schema.exclusiveMaximum`` is specified and it is number, the ``maximum`` of result equals to
            ``schema.exclusiveMaximum`` and ``exclusive_maximum`` is True.
        """
        maximum_list = (-3, 0.0, 2.2)

        for exclusive_maximum in maximum_list:
            with self.subTest(ex_max=exclusive_maximum):
                schema = {
                    "exclusiveMaximum": exclusive_maximum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertIsNone(number_range.minimum)
                self.assertEqual(number_range.maximum, exclusive_maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertTrue(number_range.exclusive_maximum)

    def test_make_range_with_max_exMax_number(self):
        """ Normalized System Test

        When ``schema.maximum`` and ``schema.exclusiveMaximum`` are specified with number, the stricter one applies.

        assert that:
            When only ``schema.maximum > schema.exclusiveMaximum``, the ``maximum`` of result equals to
            ``schema.maximum`` and ``exclusive_maximum`` is False.
            When only ``schema.maximum <= schema.exclusiveMaximum``, the ``maximum`` of result equals to
            ``schema.exclusiveMaximum`` and ``exclusive_maximum`` is True.
        """
        param_list = ((-2.0, -2.0, -2.0, True),
                      (-2.0, -2.1, -2.1, True),
                      (-2.1, -2.0, -2.1, False),
                      (0, 0, 0, True),
                      (0, -.1, -.1, True),
                      (-.1, 0, -.1, False))

        for maximum, exclusive_maximum, expected_maximum, expected_exclusive_maximum in param_list:
            with self.subTest(maximum=maximum, ex_max=exclusive_maximum):
                schema = {
                    "maximum": maximum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                number_range = NumberRange.from_schema(schema)
                self.assertIsNone(number_range.minimum)
                self.assertEqual(number_range.maximum, expected_maximum)
                self.assertFalse(number_range.exclusive_minimum)
                self.assertEqual(number_range.exclusive_maximum, expected_exclusive_maximum)
