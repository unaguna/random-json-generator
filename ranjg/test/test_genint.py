import math
import unittest
from unittest import mock

import jsonschema

from ranjg import genint
from .._context import Context
from .._generator import IntGenerator
from .._generator.__int import _get_inclusive_integer_minimum, _get_inclusive_integer_maximum
from ranjg.error import SchemaConflictError


class TestGenint(unittest.TestCase):
    """Test class of ``genint``

    Test ``ranjg.genint``
    """

    def test_genint(self):
        """ Normalized System Test

        ``genint()`` is wrapper of ``IntGenerator#gen()``.

        assert that:
            When ``genint`` is called, then ``IntGenerator#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        params_list = (
            (None, {}, None, None),
            ({"type": "integer"}, {"type": "integer"}, None, None),
            (None, {}, _context_dummy, _context_dummy),
        )

        for schema_arg, schema_used, context_arg, context_used in params_list:
            with mock.patch('ranjg._generator.IntGenerator.gen') as mock_gen:
                genint(schema_arg, context=context_arg)
                mock_gen.assert_called_once_with(schema_used, context=context_used)


class TestIntGenerator(unittest.TestCase):
    """Test class of ``IntGenerator``

    Test ``IntGenerator``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``IntGenerator().gen(schema)`` returns integer value even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``IntGenerator().gen(schema)`` returns ``int`` value.
        """
        schema = {}
        generated = IntGenerator().gen(schema)
        self.assertIsInstance(generated, int)
        jsonschema.validate(generated, schema)

    def test_gen_with_param_minimum(self):
        """ Normalized System Test

        When ``properties.minimum`` is specified, the result number ``x`` satisfies `` x >= minimum``.

        assert that:
            When the schema has ``minimum``, ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies
            `` x >= minimum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "minimum": threshold,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_maximum(self):
        """ Normalized System Test

        When ``properties.maximum`` is specified, the result number ``x`` satisfies `` x <= maximum``.

        assert that:
            When the schema has ``maximum``, ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies
            `` x <= maximum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "maximum": threshold,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertLessEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_exclusiveMinimum(self):
        """ Normalized System Test

        When ``properties.exclusiveMinimum`` is specified by a number, the result number ``x`` satisfies
        `` x > exclusiveMinimum``.

        assert that:
            When the schema has ``properties.exclusiveMinimum`` as number, ``IntGenerator().gen(schema)`` returns
            ``int`` value ``x`` and it satisfies `` x > exclusiveMinimum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "exclusiveMinimum": threshold,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_exclusiveMaximum(self):
        """ Normalized System Test

        When ``properties.exclusiveMaximum`` is specified by a number, the result number ``x`` satisfies
        `` x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.exclusiveMaximum`` as number, ``IntGenerator().gen(schema)`` returns
            ``int`` value ``x`` and it satisfies `` x < exclusiveMaximum``.
        """
        threshold_list = (-2E+10, -4.5, -2, 0, 1.0, 2, 5.1, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "exclusiveMaximum": threshold,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertLess(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_exMin_bool(self):
        """ Semi-normalized System Test

        When ``schema.exclusiveMinimum`` is boolean value and ``schema.minimum`` is not specified,
        ``IntGenerator().gen(schema)`` ignores them.

        assert that:
            When ``schema.exclusiveMinimum`` is boolean value, IntGenerator().gen(schema) returns integer value.
        """
        exclusive_minimum_list = (False, True)
        for exclusive_minimum in exclusive_minimum_list:
            with self.subTest(exclusive_minimum=exclusive_minimum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)

    def test_gen_with_param_exMax_bool(self):
        """ Semi-normalized System Test

        When ``schema.exclusiveMaximum`` is boolean value and ``schema.maximum`` is not specified,
        ``IntGenerator().gen(schema)`` ignores them.

        assert that:
            When ``schema.exclusiveMaximum`` is boolean value, IntGenerator().gen(schema) returns integer value.
        """
        exclusive_maximum_list = (False, True)
        for exclusive_maximum in exclusive_maximum_list:
            with self.subTest(exclusive_maximum=exclusive_maximum):
                schema = {
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)

    def test_gen_with_min_exMin_true(self):
        """ Normalized System Test

        When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``True``, the result number ``x``
        satisfies `` x > minimum``.

        assert that:
            When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``True``,
            ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies `` x > minimum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": threshold,
                    "exclusiveMinimum": True,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_min_exMin_false(self):
        """ Normalized System Test

        When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``False``, the result number ``x``
        satisfies `` x >= minimum``.

        assert that:
            When ``schema.minimum`` is specified and ``schema.exclusiveMinimum`` is ``False``,
            ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies `` x >= minimum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": threshold,
                    "exclusiveMinimum": False,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_max_exMax_true(self):
        """ Normalized System Test

        When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``True``, the result number ``x``
        satisfies `` x < maximum``.

        assert that:
            When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``True``,
            ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies `` x < maximum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "maximum": threshold,
                    "exclusiveMaximum": True,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertLess(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_max_exMax_false(self):
        """ Normalized System Test

        When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``False``, the result number ``x``
        satisfies `` x <= maximum``.

        assert that:
            When ``schema.maximum`` is specified and ``schema.exclusiveMaximum`` is ``False``,
            ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies `` x <= maximum``.
        """
        threshold_list = (-2E+10, -2, 0, 1.0, 2, 2E+10)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "maximum": threshold,
                    "exclusiveMaximum": False,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertLessEqual(generated, threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_tight_min_max(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.maximum`` specified, ``IntGenerator().gen(schema)`` returns integer value
        in range [``schema.minimum``, ``schema.maximum``]. So when ``minimum`` value equals ``maximum`` value, the
        returned value equals them.

        assert that:
            When ``schema.minimum`` equals ``schema.maximum``, ``IntGenerator().gen(schema)`` returns ``int`` value
            equal to them.
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
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_gen_with_tight_min_exMax(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.exclusiveMaximum`` specified, ``IntGenerator().gen(schema)`` returns
        integer value in range [``schema.minimum``, ``schema.exclusiveMaximum``). So when ``minimum`` value equals
        ``exclusiveMaximum - 1``, the returned value equals ``minimum``.

        assert that:
            When ``schema.minimum`` equals ``schema.exclusiveMaximum - 1``, ``IntGenerator().gen(schema)`` returns
            ``int`` value equal to ``minimum``.
        """
        thresholds_list = ((-2E+10, -2E+10 + 1),
                           (-2, -2 + 1),
                           (0, 0 + 1),
                           (1.0, 1.0 + 1),
                           (2, 2 + 1),
                           (3.5, 4.5),
                           (2E+10, 2E+10 + 1))

        for minimum, exclusive_maximum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_gen_with_tight_exMin_max(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` and ``schema.maximum`` specified, ``IntGenerator().gen(schema)`` returns
        integer value in range (``schema.exclusiveMinimum``, ``schema.maximum``]. So when ``maximum`` value equals
        ``exclusiveMinimum + 1``, the returned value equals ``maximum``.

        assert that:
            When ``schema.maximum`` equals ``schema.exclusiveMinimum + 1``, ``IntGenerator().gen(schema)`` returns
            ``int`` value equal to ``maximum``.
        """
        thresholds_list = ((-2E+10 - 1, -2E+10),
                           (-2 - 1, -2),
                           (0 - 1, 0),
                           (1.0 - 1, 1.0),
                           (2 - 1, 2),
                           (3.5, 4.5),
                           (2E+10 - 1, 2E+10))

        for exclusive_minimum, maximum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, maximum=maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "maximum": maximum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, exclusive_minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_gen_with_tight_exMin_exMax(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` and ``schema.exclusiveMaximum`` specified, ``IntGenerator().gen(schema)``
        returns integer value in range (``schema.exclusiveMinimum``, ``schema.exclusiveMaximum``).
        So when ``exclusiveMinimum`` value equals ``exclusiveMaximum - 2``, the returned value is mean of them.

        assert that:
            When ``schema.exclusiveMinimum + 1`` equals ``schema.exclusiveMaximum - 1``,
            ``IntGenerator().gen(schema)`` returns ``int`` value equal to them.
        """
        thresholds_list = ((-2E+10 - 1, -2E+10 + 1),
                           (-2 - 1, -2 + 1),
                           (0 - 1, 0 + 1),
                           (1.0 - 1, 1.0 + 1),
                           (2 - 1, 2 + 1),
                           (3.5, 4.5),
                           (2E+10 - 1, 2E+10 + 1))

        for exclusive_minimum, exclusive_maximum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "exclusiveMinimum": exclusive_minimum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, exclusive_minimum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_gen_with_tight_min_max_exMinTrue(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` is ``True`` and ``schema.minimum`` specified, ``IntGenerator().gen(schema)``
        returns integer value greater than ``minimum``. So when ``schema.exclusiveMinimum`` is ``True`` and ``maximum``
        value equals ``minimum + 1``, the returned value equals ``maximum``.

        assert that:
            When``schema.exclusiveMinimum`` is ``True`` and ``schema.maximum`` equals ``schema.minimum + 1``,
            ``IntGenerator().gen(schema)`` returns ``int`` value equal to ``maximum``.
        """
        thresholds_list = ((-2E+10 - 1, -2E+10),
                           (-2 - 1, -2),
                           (0 - 1, 0),
                           (1.0 - 1, 1.0),
                           (2 - 1, 2),
                           (3.5, 4.5),
                           (2E+10 - 1, 2E+10))

        for exclusive_minimum, maximum in thresholds_list:
            with self.subTest(exclusive_minimum=exclusive_minimum, maximum=maximum):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": exclusive_minimum,
                    "exclusiveMinimum": True,
                    "maximum": maximum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreater(generated, exclusive_minimum)
                self.assertLessEqual(generated, maximum)
                jsonschema.validate(generated, schema)

    def test_gen_with_tight_min_max_exMaxTrue(self):
        """ Normalized System Test

        ``When ``schema.exclusiveMaximum`` is ``True`` and ``schema.maximum`` specified, ``IntGenerator().gen(schema)``
        returns integer value lower than ``maximum``. So when ``schema.exclusiveMaximum`` is ``True`` and ``minimum``
        value equals ``maximum - 1``, the returned value equals ``minimum``.

        assert that:
            When``schema.exclusiveMaximum`` is ``True`` and ``schema.minimum`` equals ``schema.maximum - 1``,
            ``IntGenerator().gen(schema)`` returns ``int`` value equal to ``minimum``.
        """
        thresholds_list = ((-2E+10, -2E+10 + 1),
                           (-2, -2 + 1),
                           (0, 0 + 1),
                           (1.0, 1.0 + 1),
                           (2, 2 + 1),
                           (3.5, 4.5),
                           (2E+10, 2E+10 + 1))

        for minimum, exclusive_maximum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "$schema": "http://json-schema.org/draft-04/schema",
                    "minimum": minimum,
                    "maximum": exclusive_maximum,
                    "exclusiveMaximum": True,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_conflict_min_max(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``minimum <= x <= maximum``. As a result, when ``maximum < minimum``, SchemaConflictError is
        raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum``, ``IntGenerator().gen(schema)`` raised
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_conflict_min_exMax(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.exclusiveMaximum`` are specified, the result number
        ``x`` satisfies ``minimum <= x < exclusiveMaximum``. As a result, when ``exclusiveMaximum <= minimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum => properties.exclusiveMaximum``, ``IntGenerator().gen(schema)``
            raised SchemaConflictError.
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_conflict_min_max_exMax_true(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMaximum`` is
        ``True``, the result number ``x`` satisfies ``minimum <= x < maximum``. As a result, when
        ``maximum <= minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum => properties.maximum`` and ``schema.exclusiveMaximum is True``,
            ``IntGenerator().gen(schema)`` raised SchemaConflictError.
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_conflict_min_max_exMax_false(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMaximum`` is
        ``False``, the result number ``x`` satisfies ``minimum <= x <= maximum``. As a result, when
        ``maximum < minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum`` and ``schema.exclusiveMaximum is False``,
            ``IntGenerator().gen(schema)`` raised SchemaConflictError.
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_conflict_exMin_max(self):
        """ Semi-normalized System Test

        When both ``properties.exclusiveMinimum`` and ``properties.maximum`` are specified, the result number
        ``x`` satisfies ``exclusiveMinimum < x <= maximum``. As a result, when ``maximum <= exclusiveMinimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.exclusiveMinimum => properties.maximum``, ``IntGenerator().gen(schema)``
            raised SchemaConflictError.
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_conflict_min_max_exMin_true(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMinimum`` is
        ``True``, the result number ``x`` satisfies ``minimum < x <= maximum``. As a result, when
        ``maximum <= minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum => properties.maximum`` and ``schema.exclusiveMinimum is True``,
            ``IntGenerator().gen(schema)`` raised SchemaConflictError.
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_conflict_min_max_exMin_false(self):
        """ Semi-normalized System Test

        When both ``properties.minimum`` and ``properties.maximum`` are specified and ``schema.exclusiveMinimum`` is
        ``False``, the result number ``x`` satisfies ``minimum <= x <= maximum``. As a result, when
        ``maximum < minimum``, SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minimum > properties.maximum`` and ``schema.exclusiveMinimum is False``,
            ``IntGenerator().gen(schema)`` raised SchemaConflictError.
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
                self.assertRaises(SchemaConflictError, lambda: IntGenerator().gen(schema))

    def test_gen_with_param_minimum_exclusiveMinimum(self):
        """ Normalized System Test

        When both ``properties.minimum`` and ``properties.exclusiveMinimum: number`` are specified, the result number
        ``x`` satisfies ``x >= maximum`` and ``x > exclusiveMaximum``.

        assert that:
            When the schema has ``properties.minimum`` and ``properties.exclusiveMinimum`` as number,
            ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies ``x >= minimum`` and
            ``x > exclusiveMinimum``.
        """
        thresholds_list = ((1.23E+10, 123),
                           (123, 1.23E+10))
        for minimum, exclusive_minimum in thresholds_list:
            with self.subTest(minimum=minimum, exclusive_minimum=exclusive_minimum):
                schema = {
                    "minimum": minimum,
                    "exclusiveMinimum": exclusive_minimum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertGreaterEqual(generated, minimum)
                self.assertGreater(generated, exclusive_minimum)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_maximum_exclusiveMaximum(self):
        """ Normalized System Test

        When both ``properties.maximum`` and ``properties.exclusiveMaximum: number`` are specified, the result number
        ``x`` satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.maximum`` and ``properties.exclusiveMaximum`` as number,
            ``IntGenerator().gen(schema)`` returns ``int`` value ``x`` and it satisfies ``x <= maximum`` and
            ``x < exclusiveMaximum``.
        """
        thresholds_list = ((1.23E+10, 123),
                           (123, 1.23E+10))
        for maximum, exclusive_maximum in thresholds_list:
            with self.subTest(maximum=maximum, exclusive_maximum=exclusive_maximum):
                schema = {
                    "maximum": maximum,
                    "exclusiveMaximum": exclusive_maximum,
                }
                generated = IntGenerator().gen(schema)
                self.assertIsInstance(generated, int)
                self.assertLessEqual(generated, maximum)
                self.assertLess(generated, exclusive_maximum)
                jsonschema.validate(generated, schema)


class TestGenintMinimum(unittest.TestCase):
    """Test class of ``__genint._get_inclusive_integer_minimum``

    Test ``ranjg.__genint._get_inclusive_integer_minimum``. This function returns a minimum value of the value to
    generate by ``genint``.
    """

    def test_int_minimum_with_empty_schema(self):
        """ Normalized System Test

        When ``schema`` is empty, the minimum are not defined. So the range has no lower bound.

        assert that:
            When ``schema`` is empty, ``_get_inclusive_integer_range(schema)`` returns ``None``.
        """
        schema = {}
        minimum = _get_inclusive_integer_minimum(schema)
        self.assertIsNone(minimum)

    def test_int_minimum_with_min(self):
        """ Normalized System Test

        When ``schema`` has key ``minimum`` and has no key ``exclusiveMinimum``, the range is [minimum, X)
        = [ceil(minimum), X).

        assert that:
            When ``schema`` has only key ``minimum``, ``_get_inclusive_integer_range(schema)`` returns
            ``ceil(minimum)``.
        """
        schema_minimum_list = (-10.0, -5, -2.7, -2.3, 0, 3.1, 3.8, 5, 10.0)
        expected_minimum_list = map(lambda x: int(math.ceil(x)), schema_minimum_list)

        for schema_minimum, expected_minimum in zip(schema_minimum_list, expected_minimum_list):
            with self.subTest(schema_minimum=schema_minimum, expected_minimum=expected_minimum):
                schema = {
                    "minimum": schema_minimum,
                }
                minimum = _get_inclusive_integer_minimum(schema)
                self.assertEqual(minimum, expected_minimum)

    def test_int_minimum_with_exMin(self):
        """ Normalized System Test

        When ``schema`` has key ``exclusiveMinimum`` and has no key ``minimum``, the range is (exclusiveMinimum, X)
        = [floor(exclusiveMinimum)+1, X).

        assert that:
            When ``schema`` has only key ``exclusiveMinimum``, ``_get_inclusive_integer_range(schema)`` returns
            ``floor(exclusiveMinimum)+1``.
        """
        schema_minimum_list = (-10.0, -5, -2.7, -2.3, 0, 3.1, 3.8, 5, 10.0)
        expected_minimum_list = map(lambda x: int(math.floor(x) + 1), schema_minimum_list)

        for schema_exclusive_minimum, expected_minimum in zip(schema_minimum_list, expected_minimum_list):
            with self.subTest(schema_exclusive_minimum=schema_exclusive_minimum, expected_minimum=expected_minimum):
                schema = {
                    "exclusiveMinimum": schema_exclusive_minimum,
                }
                minimum = _get_inclusive_integer_minimum(schema)
                self.assertEqual(minimum, expected_minimum)

    def test_int_minimum_with_min_exMin_bool(self):
        """ Normalized System Test

        When ``schema`` has key ``minimum`` and ``schema.exclusiveMinimum == True``, the range is (minimum, X)
        = [floor(minimum)+1, X).

        When ``schema`` has key ``minimum`` and ``schema.exclusiveMinimum == False``, the range is [minimum, X)
        = [ceil(minimum), X).

        assert that:
            When ``schema`` has key ``minimum`` and ``schema.exclusiveMinimum`` is boolean value,
            ``_get_inclusive_integer_range(schema)`` returns ``floor(minimum)+1`` with ``schema.exclusiveMinimum=True``
            or returns ``ceil(minimum)`` with ``schema.exclusiveMinimum=False``.
        """
        parameter_list = ((-10.0, True, -9),
                          (-10.0, False, -10),
                          (-5, True, -4),
                          (-5, False, -5),
                          (-2.7, True, -2),
                          (-2.7, False, -2),
                          (-2.3, True, -2),
                          (-2.3, False, -2),
                          (0, True, 1),
                          (0, False, 0),
                          (3.1, True, 4),
                          (3.1, False, 4),
                          (3.8, True, 4),
                          (3.8, False, 4),
                          (5, True, 6),
                          (5, False, 5),
                          (10.0, True, 11),
                          (10.0, False, 10))

        for schema_minimum, schema_exclusive_minimum, expected_minimum in parameter_list:
            with self.subTest(schema_minimum=schema_minimum,
                              exclusive=str(schema_exclusive_minimum)[0],
                              expected_minimum=expected_minimum):
                schema = {
                    "minimum": schema_minimum,
                    "exclusiveMinimum": schema_exclusive_minimum,
                }
                minimum = _get_inclusive_integer_minimum(schema)
                self.assertEqual(minimum, expected_minimum)

    def test_int_minimum_with_min_exMin(self):
        """ Normalized System Test

        When ``schema`` has key ``minimum`` and ``schema.exclusiveMinimum``, the range satisfies both of them.
        In other words, if ``minimum <= exclusiveMinimum`` then the range is (exclusiveMinimum, X) , otherwise
        the range is [minimum, X).

        assert that:
            When ``schema.minimum <= schema.exclusiveMinimum``,
            ``_get_inclusive_integer_range(schema)`` returns ``floor(exclusiveMinimum)+1`.
            When ``schema.minimum > schema.exclusiveMinimum``,
            ``_get_inclusive_integer_range(schema)`` returns ``ceil(minimum)`.
        """
        parameter_list = ((1, 2, 3),
                          (1, 1, 2),
                          (2, 1, 2),
                          (1.1, 1.2, 2),
                          (1.1, 1.1, 2),
                          (1.2, 1.1, 2),
                          (-1.5, -1.0, 0),
                          (-1.0, -1.5, -1))

        for schema_minimum, schema_exclusive_minimum, expected_minimum in parameter_list:
            with self.subTest(schema_minimum=schema_minimum,
                              schema_exclusive_minimum=schema_exclusive_minimum,
                              expected_minimum=expected_minimum):
                schema = {
                    "minimum": schema_minimum,
                    "exclusiveMinimum": schema_exclusive_minimum,
                }
                minimum = _get_inclusive_integer_minimum(schema)
                self.assertEqual(minimum, expected_minimum)


class TestGenintMaximum(unittest.TestCase):
    """Test class of ``__genint._get_inclusive_integer_maximum``

    Test ``ranjg.__genint._get_inclusive_integer_maximum``. This function returns a maximum value of the value to
    generate by ``genint``.
    """

    def test_int_maximum_with_empty_schema(self):
        """ Normalized System Test

        When ``schema`` is empty, the maximum are not defined. So the range has no upper bound.

        assert that:
            When ``schema`` is empty, ``_get_inclusive_integer_range(schema)`` returns ``None``.
        """
        schema = {}
        maximum = _get_inclusive_integer_maximum(schema)
        self.assertIsNone(maximum)

    def test_int_maximum_with_min(self):
        """ Normalized System Test

        When ``schema`` has key ``maximum`` and has no key ``exclusiveMaximum``, the range is [maximum, X)
        = [floor(maximum), X).

        assert that:
            When ``schema`` has only key ``maximum``, ``_get_inclusive_integer_range(schema)`` returns
            ``floor(maximum)``.
        """
        schema_maximum_list = (-10.0, -5, -2.7, -2.3, 0, 3.1, 3.8, 5, 10.0)
        expected_maximum_list = map(lambda x: int(math.floor(x)), schema_maximum_list)

        for schema_maximum, expected_maximum in zip(schema_maximum_list, expected_maximum_list):
            with self.subTest(schema_maximum=schema_maximum, expected_maximum=expected_maximum):
                schema = {
                    "maximum": schema_maximum,
                }
                maximum = _get_inclusive_integer_maximum(schema)
                self.assertEqual(maximum, expected_maximum)

    def test_int_maximum_with_exMin(self):
        """ Normalized System Test

        When ``schema`` has key ``exclusiveMaximum`` and has no key ``maximum``, the range is (exclusiveMaximum, X)
        = [ceil(exclusiveMaximum)-1, X).

        assert that:
            When ``schema`` has only key ``exclusiveMaximum``, ``_get_inclusive_integer_range(schema)`` returns
            ``ceil(exclusiveMaximum)-1``.
        """
        schema_maximum_list = (-10.0, -5, -2.7, -2.3, 0, 3.1, 3.8, 5, 10.0)
        expected_maximum_list = map(lambda x: int(math.ceil(x) - 1), schema_maximum_list)

        for schema_exclusive_maximum, expected_maximum in zip(schema_maximum_list, expected_maximum_list):
            with self.subTest(schema_exclusive_maximum=schema_exclusive_maximum, expected_maximum=expected_maximum):
                schema = {
                    "exclusiveMaximum": schema_exclusive_maximum,
                }
                maximum = _get_inclusive_integer_maximum(schema)
                self.assertEqual(maximum, expected_maximum)

    def test_int_maximum_with_min_exMin_bool(self):
        """ Normalized System Test

        When ``schema`` has key ``maximum`` and ``schema.exclusiveMaximum == True``, the range is (maximum, X)
        = [ceil(maximum)-1, X).

        When ``schema`` has key ``maximum`` and ``schema.exclusiveMaximum == False``, the range is [maximum, X)
        = [floor(maximum), X).

        assert that:
            When ``schema`` has key ``maximum`` and ``schema.exclusiveMaximum`` is boolean value,
            ``_get_inclusive_integer_range(schema)`` returns ``ceil(maximum)-1`` with ``schema.exclusiveMaximum=True``
            or returns ``floor(maximum)`` with ``schema.exclusiveMaximum=False``.
        """
        parameter_list = ((-10.0, True, -11),
                          (-10.0, False, -10),
                          (-5, True, -6),
                          (-5, False, -5),
                          (-2.7, True, -3),
                          (-2.7, False, -3),
                          (-2.3, True, -3),
                          (-2.3, False, -3),
                          (0, True, -1),
                          (0, False, 0),
                          (3.1, True, 3),
                          (3.1, False, 3),
                          (3.8, True, 3),
                          (3.8, False, 3),
                          (5, True, 4),
                          (5, False, 5),
                          (10.0, True, 9),
                          (10.0, False, 10))

        for schema_maximum, schema_exclusive_maximum, expected_maximum in parameter_list:
            with self.subTest(schema_maximum=schema_maximum,
                              exclusive=str(schema_exclusive_maximum)[0],
                              expected_maximum=expected_maximum):
                schema = {
                    "maximum": schema_maximum,
                    "exclusiveMaximum": schema_exclusive_maximum,
                }
                maximum = _get_inclusive_integer_maximum(schema)
                self.assertEqual(maximum, expected_maximum)

    def test_int_maximum_with_min_exMin(self):
        """ Normalized System Test

        When ``schema`` has key ``maximum`` and ``schema.exclusiveMaximum``, the range satisfies both of them.
        In other words, if ``maximum <= exclusiveMaximum`` then the range is (exclusiveMaximum, X) , otherwise
        the range is [maximum, X).

        assert that:
            When ``schema.maximum <= schema.exclusiveMaximum``,
            ``_get_inclusive_integer_range(schema)`` returns ``ceil(exclusiveMaximum)-1`.
            When ``schema.maximum > schema.exclusiveMaximum``,
            ``_get_inclusive_integer_range(schema)`` returns ``floor(maximum)`.
        """
        parameter_list = ((1, 2, 1),
                          (1, 1, 0),
                          (2, 1, 0),
                          (1.1, 1.2, 1),
                          (1.1, 1.1, 1),
                          (1.2, 1.1, 1),
                          (-1.5, -1.0, -2),
                          (-1.0, -1.5, -2))

        for schema_maximum, schema_exclusive_maximum, expected_maximum in parameter_list:
            with self.subTest(schema_maximum=schema_maximum,
                              schema_exclusive_maximum=schema_exclusive_maximum,
                              expected_maximum=expected_maximum):
                schema = {
                    "maximum": schema_maximum,
                    "exclusiveMaximum": schema_exclusive_maximum,
                }
                maximum = _get_inclusive_integer_maximum(schema)
                self.assertEqual(maximum, expected_maximum)
