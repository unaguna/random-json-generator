import unittest

import jsonschema

from ranjg import gennum
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
