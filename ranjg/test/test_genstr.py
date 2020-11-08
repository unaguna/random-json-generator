import unittest
import jsonschema
from ranjg import genstr
from ranjg.error import InvalidSchemaError, SchemaConflictError


class TestGenstr(unittest.TestCase):
    """Test class of ``genstr``

    Test ``ranjg.genstr``
    """

    def test_genstr_with_empty_schema(self):
        """ Normalized System Test

        ``genstr(schema)`` returns a string value. When ``schema`` is empty, the result contains only alphabets.

        assert that:
            When the schema is empty, ``genstr(schema)`` returns ``str`` value contains only alphabets.
        """
        schema = {}
        generated = genstr(schema)
        self.assertIsInstance(generated, str)
        self.assertTrue(generated.isalpha())
        jsonschema.validate(generated, schema)

    def test_genstr_with_maxLength_0(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``genstr(schema)`` returns a string value with a length of ``maxLength``
        or less.

        assert that:
            When ``schema.maxLength == 0``, ``genstr(schema)`` returns the empty string.
        """
        schema = {"maxLength": 0}
        generated = genstr(schema)
        self.assertEqual(generated, "")
        jsonschema.validate(generated, schema)

    def test_genstr_with_maxLength(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``genstr(schema)`` returns a string value with a length of ``maxLength``
        or less.

        assert that:
            When ``schema.maxLength``, ``genstr(schema)`` returns a string with a length of ``maxLength`` or less.
        """
        threshold_list = (1, 2, 3, 1.0)

        for max_length in threshold_list:
            with self.subTest(max_length=max_length):
                schema = {"maxLength": max_length}
                generated = genstr(schema)
                self.assertIsInstance(generated, str)
                self.assertLessEqual(len(generated), max_length)
                jsonschema.validate(generated, schema)

    def test_genstr_with_negative_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be non-negative. When ``schema.maxLength < 0``, ``genstr(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.maxLength < 0``, ``genstr(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: genstr(schema))

    def test_genstr_with_non_integer_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be integer. More precisely, ``maxLength`` must be a number value divided by 1. When
        ``schema.maxLength`` cannot divided by 1, ``genstr(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.maxLength`` cannot divided by 1, ``genstr(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: genstr(schema))

    def test_genstr_with_non_number_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be number. When ``schema.maxLength`` isn't number, ``genstr(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.maxLength`` isn't number, ``genstr(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": "1"
        }
        self.assertRaises(InvalidSchemaError, lambda: genstr(schema))

    def test_genstr_with_minLength(self):
        """ Normalized System Test

        When ``schema.minLength`` is specified, ``genstr(schema)`` returns a string value with a length of ``minLength``
        or more.

        assert that:
            When ``schema.minLength`` is specified, ``genstr(schema)`` returns the string value and it's length is
            greater than or equal to ``minLength``.
        """
        threshold_list = (1, 2, 3, 1.0)

        for min_length in threshold_list:
            with self.subTest(min_length=min_length):
                schema = {"minLength": min_length}
                generated = genstr(schema)
                self.assertIsInstance(generated, str)
                self.assertGreaterEqual(len(generated), min_length)
                jsonschema.validate(generated, schema)

    def test_genstr_with_negative_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be non-negative. When ``schema.minLength < 0``, ``genstr(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.minLength < 0``, ``genstr(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: genstr(schema))

    def test_genstr_with_non_integer_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be integer. More precisely, ``minLength`` must be a number value divided by 1. When
        ``schema.minLength`` cannot divided by 1, ``genstr(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.minLength`` cannot divided by 1, ``genstr(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: genstr(schema))

    def test_genstr_with_non_number_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be number. When ``schema.minLength`` isn't number, ``genstr(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.minLength`` isn't number, ``genstr(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": "1"
        }
        self.assertRaises(InvalidSchemaError, lambda: genstr(schema))

    def test_genstr_with_length(self):
        """ Normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``genstr(schema)`` returns a string value with
        a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when ``minLength`` and ``maxLength`` have
        same value, the length of the result equals them.

        assert that:
            When ``schema.minLength`` and ``schema.maxLength`` is specified, ``genstr(schema)`` returns the string with
            a length ``x`` satisfies ``minLength <= x <= maxLength``.
        """
        thresholds_list = ((0, 1),
                           (10, 10),
                           (12, 15))

        for min_length, max_length in thresholds_list:
            with self.subTest(min_length=min_length, max_length=max_length):
                schema = {"minLength": min_length, "maxLength": max_length}
                generated = genstr(schema)
                self.assertIsInstance(generated, str)
                self.assertGreaterEqual(len(generated), min_length)
                self.assertLessEqual(len(generated), max_length)
                jsonschema.validate(generated, schema)

    def test_genstr_with_conflicting_length(self):
        """ Semi-normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``genstr(schema)`` returns a string value with
        a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when ``minLength > maxLength``,
        ``genstr(schema)`` raises SchemaConflictError.

        assert that:
            When ``schema.minLength > schema.maxLength``, ``genstr(schema)`` raises SchemaConflictError.
        """
        thresholds_list = ((0, 1),
                           (12, 15))

        for max_length, min_length in thresholds_list:
            with self.subTest(min_length=min_length, max_length=max_length):
                schema = {"minLength": min_length, "maxLength": max_length}
                self.assertRaises(SchemaConflictError, lambda: genstr(schema))

    def test_genstr_with_pattern(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression.

        assert that:
            When ``schema.pattern`` is valid as regular expression, ``genstr(schema)`` returns a string satisfies this
            regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z]+\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern}
                generated = genstr(schema)
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                jsonschema.validate(generated, schema)

    def test_genstr_with_illegal_pattern(self):
        """ Semi-normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression. As a result,
        when ``schema.pattern`` is invalid as regular expression, ``genstr(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.pattern`` is invalid as regular expression, ``genstr(schema)`` raises InvalidSchemaError.
        """
        pattern_list = ("[0-1",
                        "\\")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern}
                self.assertRaises(InvalidSchemaError, lambda: genstr(schema))
