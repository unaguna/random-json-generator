import unittest
import jsonschema
from ranjg import genint
from ranjg.error import SchemaConflictError, InvalidSchemaError


class TestGenint(unittest.TestCase):
    """Test class of ``genint``

    Test ``ranjg.genint``
    """

    def test_genint_with_empty_schema(self):
        """ Normalized System Test

        ``genint(schema)`` returns integer value even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``genint(schema)`` returns ``int`` value.
        """
        schema = {}
        generated = genint(schema)
        self.assertIsInstance(generated, int)
        jsonschema.validate(generated, schema)

    def test_genint_with_param_minimum(self):
        """ Normalized System Test

        When ``properties.minimum`` is specified, the result number ``x`` satisfies `` x >= minimum``.

        assert that:
            When the schema has ``minimum``, ``genint(schema)`` returns ``int`` value ``x`` and it satisfies
            `` x >= minimum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "minimum": threshold,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_param_maximum(self):
        """ Normalized System Test

        When ``properties.maximum`` is specified, the result number ``x`` satisfies `` x <= maximum``.

        assert that:
            When the schema has ``maximum``, ``genint(schema)`` returns ``int`` value ``x`` and it satisfies
            `` x <= maximum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "maximum": threshold,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertLessEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_param_exclusiveMinimum(self):
        """ Normalized System Test

        When ``properties.exclusiveMinimum`` is specified by a number, the result number ``x`` satisfies
        `` x > exclusiveMinimum``.

        assert that:
            When the schema has ``properties.exclusiveMinimum`` as number, ``genint(schema)`` returns ``int`` value
            ``x`` and it satisfies `` x > exclusiveMinimum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "exclusiveMinimum": threshold,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_param_exclusiveMaximum(self):
        """ Normalized System Test

        When ``properties.exclusiveMaximum`` is specified by a number, the result number ``x`` satisfies
        `` x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.exclusiveMaximum`` as number, ``genint(schema)`` returns ``int`` value
            ``x`` and it satisfies `` x < exclusiveMaximum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "exclusiveMaximum": threshold,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertLess(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_param_exMin_bool(self):
        """ Semi-normalized System Test

        When ``schema.exclusiveMinimum`` is boolean value, ``schema.minimum`` is required. As a result, when
        ``schema.exclusiveMinimum`` is boolean value and ``schema.minimum`` is not specified, genint(schema) raises
        SchemaConflictError.

        assert that:
            When ``schema.exclusiveMinimum`` is boolean value and ``schema.minimum`` is not specified, genint(schema)
            raises InvalidSchemaError.
        """
        exclusive_minimum_list = (False, True)
        for exclusive_minimum in exclusive_minimum_list:
            with self.subTest(exclusive_minimum=exclusive_minimum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                }
                self.assertRaises(InvalidSchemaError, lambda: genint(schema))

    def test_genint_with_param_exMax_bool(self):
        """ Semi-normalized System Test

        When ``schema.exclusiveMaximum`` is boolean value, ``schema.maximum`` is required. As a result, when
        ``schema.exclusiveMaximum`` is boolean value and ``schema.maximum`` is not specified, genint(schema) raises
        SchemaConflictError.

        assert that:
            When ``schema.exclusiveMaximum`` is boolean value and ``schema.maximum`` is not specified, genint(schema)
            raises InvalidSchemaError.
        """
        exclusive_maximum_list = (False, True)
        for exclusive_maximum in exclusive_maximum_list:
            with self.subTest(exclusive_maximum=exclusive_maximum):
                schema = {
                    "exclusiveMaximum": exclusive_maximum,
                }
                self.assertRaises(InvalidSchemaError, lambda: genint(schema))

    def test_genint_with_min_exMin_true(self):
        """ Normalized System Test

        When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``True``, the result number ``x``
        satisfies `` x > minimum``.

        assert that:
            When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``True``, ``genint(schema)`` returns
            ``int`` value ``x`` and it satisfies `` x > minimum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": threshold,
                    "exclusiveMinimum": True,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_min_exMin_false(self):
        """ Normalized System Test

        When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``False``, the result number ``x``
        satisfies `` x >= minimum``.

        assert that:
            When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``False``, ``genint(schema)``
            returns ``int`` value ``x`` and it satisfies `` x >= minimum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": threshold,
                    "exclusiveMinimum": False,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_max_exMax_true(self):
        """ Normalized System Test

        When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``True``, the result number ``x``
        satisfies `` x < maximum``.

        assert that:
            When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``True``, ``genint(schema)`` returns
            ``int`` value ``x`` and it satisfies `` x < maximum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "maximum": threshold,
                    "exclusiveMaximum": True,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertLess(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_max_exMax_false(self):
        """ Normalized System Test

        When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``False``, the result number ``x``
        satisfies `` x <= maximum``.

        assert that:
            When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``False``, ``genint(schema)``
            returns ``int`` value ``x`` and it satisfies `` x <= maximum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "maximum": threshold,
                    "exclusiveMaximum": False,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertLessEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_genint_with_tight_min_max(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.maximum`` specified, ``genint(schema)`` returns integer value in range
        [``schema.minimum``, ``schema.maximum``]. So when ``minimum`` value equals ``maximum`` value, the returned value
        equals them.

        assert that:
            When ``schema.minimum`` equals ``schema.maximum``, ``genint(schema)`` returns ``int`` value equal to them.
        """
        thresholds_list = ((-2E+10, -2E+10),
                           (-2, -2),
                           (0, 0),
                           (1.0, 1.0),
                           (2, 2),
                           (3.5, 4.5),
                           (2E+10, 2E+10))

        for minimum, maximum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_genint_with_tight_min_exMax(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.exclusiveMaximum`` specified, ``genint(schema)`` returns integer value in
        range [``schema.minimum``, ``schema.exclusiveMaximum``). So when ``minimum`` value equals
        ``exclusiveMaximum - 1``, the returned value equals ``minimum``.

        assert that:
            When ``schema.minimum`` equals ``schema.exclusiveMaximum - 1``, ``genint(schema)`` returns ``int`` value
            equal to ``minimum``.
        """
        thresholds_list = ((-2E+10, -2E+10+1),
                           (-2, -2+1),
                           (0, 0+1),
                           (1.0, 1.0+1),
                           (2, 2+1),
                           (3.5, 4.5),
                           (2E+10, 2E+10+1))

        for minimum, exclusive_maximum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_genint_with_tight_exMin_max(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` and ``schema.maximum`` specified, ``genint(schema)`` returns integer value in
        range (``schema.exclusiveMinimum``, ``schema.maximum``]. So when ``maximum`` value equals
        ``exclusiveMinimum + 1``, the returned value equals ``maximum``.

        assert that:
            When ``schema.maximum`` equals ``schema.exclusiveMinimum + 1``, ``genint(schema)`` returns ``int`` value
            equal to ``maximum``.
        """
        thresholds_list = ((-2E+10-1, -2E+10),
                           (-2-1, -2),
                           (0-1, 0),
                           (1.0-1, 1.0),
                           (2-1, 2),
                           (3.5, 4.5),
                           (2E+10-1, 2E+10))

        for exclusive_minimum, maximum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, maximum=maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "maximum": maximum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, exclusive_minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_genint_with_tight_exMin_exMax(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` and ``schema.exclusiveMaximum`` specified, ``genint(schema)`` returns integer
        value in range (``schema.exclusiveMinimum``, ``schema.exclusiveMaximum``). So when ``exclusiveMinimum`` value
        equals ``exclusiveMaximum - 2``, the returned value is mean of them.

        assert that:
            When ``schema.exclusiveMinimum + 1`` equals ``schema.exclusiveMaximum - 1``, ``genint(schema)`` returns
            ``int`` value equal to them.
        """
        thresholds_list = ((-2E+10-1, -2E+10+1),
                           (-2-1, -2+1),
                           (0-1, 0+1),
                           (1.0-1, 1.0+1),
                           (2-1, 2+1),
                           (3.5, 4.5),
                           (2E+10-1, 2E+10+1))

        for exclusive_minimum, exclusive_maximum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, exclusive_minimum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_genint_with_tight_min_max_exMinTrue(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` is ``True`` and ``schema.minimum`` specified, ``genint(schema)`` returns
        integer value greater than ``minimum``. So when ``schema.exclusiveMinimum`` is ``True`` and ``maximum`` value
        equals ``minimum + 1``, the returned value equals ``maximum``.

        assert that:
            When``schema.exclusiveMinimum`` is ``True`` and ``schema.maximum`` equals ``schema.minimum + 1``,
            ``genint(schema)`` returns ``int`` value equal to ``maximum``.
        """
        thresholds_list = ((-2E+10-1, -2E+10),
                           (-2-1, -2),
                           (0-1, 0),
                           (1.0-1, 1.0),
                           (2-1, 2),
                           (3.5, 4.5),
                           (2E+10-1, 2E+10))

        for exclusive_minimum, maximum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, maximum=maximum):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": exclusive_minimum,
                    "exclusiveMinimum": True,
                    "maximum": maximum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, exclusive_minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_genint_with_tight_min_max_exMaxTrue(self):
        """ Normalized System Test

        ``When ``schema.exclusiveMaximum`` is ``True`` and ``schema.maximum`` specified, ``genint(schema)`` returns
        integer value lower than ``maximum``. So when ``schema.exclusiveMaximum`` is ``True`` and ``minimum`` value
        equals ``maximum - 1``, the returned value equals ``minimum``.

        assert that:
            When``schema.exclusiveMaximum`` is ``True`` and ``schema.minimum`` equals ``schema.maximum - 1``,
            ``genint(schema)`` returns ``int`` value equal to ``minimum``.
        """
        thresholds_list = ((-2E+10, -2E+10+1),
                           (-2, -2+1),
                           (0, 0+1),
                           (1.0, 1.0+1),
                           (2, 2+1),
                           (3.5, 4.5),
                           (2E+10, 2E+10+1))

        for minimum, exclusive_maximum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": minimum,
                    "maximum": exclusive_maximum,
                    "exclusiveMaximum": True,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_genint_with_param_conflict_min_max(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``minimum <= x <= maximum``. As a result, when ``maximum < minimum``, SchemaConflictError is
        raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum``, ``genint(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, 0),
                           (-10, 10),
                           (0, 10),
                           (1.9, 1.1),
                           (5, 10))
        for maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_conflict_min_exMax(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.exclusiveMaximum`` are specified, the result number
        ``x`` satisfies ``minimum <= x < exclusiveMaximum``. As a result, when ``exclusiveMaximum <= minimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum => properties.exclusiveMaximum``, ``genint(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, -10),
                           (-10, 0),
                           (-10, 10),
                           (0, 0),
                           (0, 10),
                           (2.0, 1.1),
                           (5, 10),
                           (10, 10))
        for exclusive_maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, exclusiveMaximum=exclusive_maximum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_conflict_min_max_exMax_true(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMaximum`` is
        ``True``, the result number ``x`` satisfies ``minimum <= x < maximum``. As a result, when
        ``maximum <= minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum => properties.maximum`` and ``schema.exclusiveMaximum is True``,
            ``genint(schema)`` raised SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, -10),
                           (-10, 0),
                           (-10, 10),
                           (0, 0),
                           (0, 10),
                           (2.0, 1.1),
                           (5, 10),
                           (10, 10))
        for maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                    "exclusiveMaximum": True,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_conflict_min_max_exMax_false(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMaximum`` is
        ``False``, the result number ``x`` satisfies ``minimum <= x <= maximum``. As a result, when
        ``maximum < minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum`` and ``schema.exclusiveMaximum is False``,
            ``genint(schema)`` raised SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, 0),
                           (-10, 10),
                           (0, 10),
                           (1.9, 1.1),
                           (5, 10))
        for maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                    "exclusiveMaximum": False,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_conflict_exMin_max(self):
        """ Semi-normalized System Test

        When both ``properties.exclusiveMinimum`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``exclusiveMinimum < x <= maximum``. As a result, when ``maximum <= exclusiveMinimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.exclusiveMinimum => properties.maximum``, ``genint(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, -10),
                           (-10, 0),
                           (-10, 10),
                           (0, 0),
                           (0, 10),
                           (1.9, 1.0),
                           (5, 10),
                           (10, 10))
        for maximum, exclusive_minimum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, maximum=maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "maximum": maximum,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_conflict_min_max_exMin_true(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMinimum`` is
        ``True``, the result number ``x`` satisfies ``minimum < x <= maximum``. As a result, when
        ``maximum <= minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum => properties.maximum`` and ``schema.exclusiveMinimum is True``,
            ``genint(schema)`` raised SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, -10),
                           (-10, 0),
                           (-10, 10),
                           (0, 0),
                           (0, 10),
                           (1.9, 1.0),
                           (5, 10),
                           (10, 10))
        for maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                    "exclusiveMinimum": True,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_conflict_min_max_exMin_false(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMinimum`` is
        ``False``, the result number ``x`` satisfies ``minimum <= x <= maximum``. As a result, when
        ``maximum < minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum`` and ``schema.exclusiveMinimum is False``,
            ``genint(schema)`` raised SchemaConflictError.
        """
        thresholds_list = ((-10, -5),
                           (-10, 0),
                           (-10, 10),
                           (0, 10),
                           (1.9, 1.1),
                           (5, 10))
        for maximum, minimum in thresholds_list:
            with self.subTest(minimum=minimum, maximum=maximum):
                schema = {
                    "minimum": minimum,
                    "maximum": maximum,
                    "exclusiveMinimum": False,
                }
                self.assertRaises(SchemaConflictError, lambda: genint(schema))

    def test_genint_with_param_minimum_exclusiveMinimum(self):
        """ Normalized System Test

        When both ``properties.minimum`` and ``properties.exclusiveMinimum: number`` are specified, the result number
        ``x`` satisfies ``x >= maximum`` and ``x > exclusiveMaximum``.

        assert that:
            When the schema has ``properties.minimum`` and ``properties.exclusiveMinimum`` as number, ``genint(schema)``
            returns ``int`` value ``x`` and it satisfies ``x >= minimum`` and ``x > exclusiveMinimum``.
        """
        thresholds_list = ((1.23E+10, 123),
                           (123, 1.23E+10))
        for minimum, exclusive_minimum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_minimum=exclusive_minimum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMinimum": exclusive_minimum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertGreater(generated, exclusive_minimum)
                jsonschema.validate(generated, schema)

    def test_genint_with_param_maximum_exclusiveMaximum(self):
        """ Normalized System Test

        When both ``properties.maximum`` and ``properties.exclusiveMaximum: number`` are specified, the result number
        ``x`` satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.maximum`` and ``properties.exclusiveMaximum`` as number, ``genint(schema)``
            returns ``int`` value ``x`` and it satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.
        """
        thresholds_list = ((1.23E+10, 123),
                           (123, 1.23E+10))
        for maximum, exclusive_maximum in thresholds_list:
            with self.subTest(maximum=maximum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "maximum": maximum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = genint(schema)
                self.assertIsInstance(generated, int)
                self.assertLessEqual(generated, maximum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)
