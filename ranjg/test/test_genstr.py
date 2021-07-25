import unittest
from unittest import mock

import jsonschema
from ranjg import genstr
from .._context import Context
from .._generator import StrGenerator
from ranjg.error import InvalidSchemaError, SchemaConflictError


class TestGenstr(unittest.TestCase):
    """Test class of ``genstr``

    Test ``ranjg.genstr``
    """

    def test_genstr(self):
        """ Normalized System Test

        ``genstr()`` is wrapper of ``StrGenerator#gen()``.

        assert that:
            When ``genstr`` is called, then ``StrGenerator#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        params_list = (
            (None, None, False),
            ({"type": "array"}, None, False),
            ({"type": "array"}, None, True),
            (None, _context_dummy, False),
        )

        for schema, context, is_validated in params_list:
            with mock.patch('ranjg._generator.StrGenerator.gen') as mock_gen:
                genstr(schema, context=context, schema_is_validated=is_validated)
                mock_gen.assert_called_once_with(schema, context=context, schema_is_validated=is_validated)


class TestStrGenerator(unittest.TestCase):
    """Test class of ``StrGenerator``

    Test ``StrGenerator``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``StrGenerator().gen(schema)`` returns a string value. When ``schema`` is empty, the result contains only
        alphabets.

        assert that:
            When the schema is empty, ``StrGenerator().gen(schema)`` returns ``str`` value contains only alphabets.
        """
        schema = {}
        generated = StrGenerator().gen(schema)
        self.assertIsInstance(generated, str)
        self.assertTrue(generated.isalpha())
        jsonschema.validate(generated, schema)

    def test_gen_with_maxLength_0(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``StrGenerator().gen(schema)`` returns a string value with a length of
        ``maxLength`` or less.

        assert that:
            When ``schema.maxLength == 0``, ``StrGenerator().gen(schema)`` returns the empty string.
        """
        schema = {"maxLength": 0}
        generated = StrGenerator().gen(schema)
        self.assertEqual(generated, "")
        jsonschema.validate(generated, schema)

    def test_gen_with_maxLength(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``StrGenerator().gen(schema)`` returns a string value with a length of
        ``maxLength`` or less.

        assert that:
            When ``schema.maxLength``, ``StrGenerator().gen(schema)`` returns a string with a length of ``maxLength`` or
            less.
        """
        threshold_list = (1, 2, 3, 1.0)

        for max_length in threshold_list:
            with self.subTest(max_length=max_length):
                schema = {"maxLength": max_length}
                generated = StrGenerator().gen(schema)
                self.assertIsInstance(generated, str)
                self.assertLessEqual(len(generated), max_length)
                jsonschema.validate(generated, schema)

    def test_gen_with_negative_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be non-negative. When ``schema.maxLength < 0``, ``StrGenerator().gen(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.maxLength < 0``, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))

    def test_gen_with_non_integer_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be integer. More precisely, ``maxLength`` must be a number value divided by 1. When
        ``schema.maxLength`` cannot divided by 1, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.maxLength`` cannot divided by 1, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))

    def test_gen_with_non_number_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be number. When ``schema.maxLength`` isn't number, ``StrGenerator().gen(schema)``
        raises InvalidSchemaError.

        assert that:
            When ``schema.maxLength`` isn't number, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": "1"
        }
        self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))

    def test_gen_with_minLength(self):
        """ Normalized System Test

        When ``schema.minLength`` is specified, ``StrGenerator().gen(schema)`` returns a string value with a length of
        ``minLength`` or more.

        assert that:
            When ``schema.minLength`` is specified, ``StrGenerator().gen(schema)`` returns the string value and it's
            length is greater than or equal to ``minLength``.
        """
        threshold_list = (1, 2, 3, 1.0)

        for min_length in threshold_list:
            with self.subTest(min_length=min_length):
                schema = {"minLength": min_length}
                generated = StrGenerator().gen(schema)
                self.assertIsInstance(generated, str)
                self.assertGreaterEqual(len(generated), min_length)
                jsonschema.validate(generated, schema)

    def test_gen_with_negative_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be non-negative. When ``schema.minLength < 0``, ``StrGenerator().gen(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.minLength < 0``, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))

    def test_gen_with_non_integer_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be integer. More precisely, ``minLength`` must be a number value divided by 1. When
        ``schema.minLength`` cannot divided by 1, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.minLength`` cannot divided by 1, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))

    def test_gen_with_non_number_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be number. When ``schema.minLength`` isn't number, ``StrGenerator().gen(schema)``
        raises InvalidSchemaError.

        assert that:
            When ``schema.minLength`` isn't number, ``StrGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": "1"
        }
        self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))

    def test_gen_with_length(self):
        """ Normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``StrGenerator().gen(schema)`` returns a string
        value with a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when ``minLength`` and
        ``maxLength`` have same value, the length of the result equals them.

        assert that:
            When ``schema.minLength`` and ``schema.maxLength`` is specified, ``StrGenerator().gen(schema)`` returns the
            string with a length ``x`` satisfies ``minLength <= x <= maxLength``.
        """
        thresholds_list = ((0, 1),
                           (10, 10),
                           (12, 15))

        for min_length, max_length in thresholds_list:
            with self.subTest(min_length=min_length, max_length=max_length):
                schema = {"minLength": min_length, "maxLength": max_length}
                generated = StrGenerator().gen(schema)
                self.assertIsInstance(generated, str)
                self.assertGreaterEqual(len(generated), min_length)
                self.assertLessEqual(len(generated), max_length)
                jsonschema.validate(generated, schema)

    def test_gen_with_conflicting_length(self):
        """ Semi-normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``StrGenerator().gen(schema)`` returns a string
        value with a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when
        ``minLength > maxLength``, ``StrGenerator().gen(schema)`` raises SchemaConflictError.

        assert that:
            When ``schema.minLength > schema.maxLength``, ``StrGenerator().gen(schema)`` raises SchemaConflictError.
        """
        thresholds_list = ((0, 1),
                           (12, 15))

        for max_length, min_length in thresholds_list:
            with self.subTest(min_length=min_length, max_length=max_length):
                schema = {"minLength": min_length, "maxLength": max_length}
                self.assertRaises(SchemaConflictError, lambda: StrGenerator().gen(schema))

    def test_gen_with_pattern(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression.

        assert that:
            When ``schema.pattern`` is valid as regular expression, ``StrGenerator().gen(schema)`` returns a string
            satisfies this regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z]+\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern}
                generated = StrGenerator().gen(schema)
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                jsonschema.validate(generated, schema)

    def test_gen_with_pattern_and_minLength(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression even if it
        contradicts ``schema.minLength``.

        assert that:
            When ``schema.pattern`` is valid as regular expression and ``schema.minLength`` contradicts ``pattern``,
            ``StrGenerator().gen(schema)`` returns a string satisfies this regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z][A-Z]\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern, "minLength": 13}
                generated = StrGenerator().gen(schema)
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                self.assertRaises(jsonschema.ValidationError, lambda: jsonschema.validate(generated, schema))

    def test_gen_with_pattern_and_maxLength(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression even if it
        contradicts ``schema.maxLength``.

        assert that:
            When ``schema.pattern`` is valid as regular expression and ``schema.maxLength`` contradicts ``pattern``,
            ``StrGenerator().gen(schema)`` returns a string satisfies this regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z][A-Z]\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern, "maxLength": 3}
                generated = StrGenerator().gen(schema)
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                self.assertRaises(jsonschema.ValidationError, lambda: jsonschema.validate(generated, schema))

    def test_gen_with_illegal_pattern(self):
        """ Semi-normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression. As a result,
        when ``schema.pattern`` is invalid as regular expression, ``StrGenerator().gen(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.pattern`` is invalid as regular expression, ``StrGenerator().gen(schema)`` raises
            InvalidSchemaError.
        """
        pattern_list = ("[0-1",
                        "\\")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern}
                self.assertRaises(InvalidSchemaError, lambda: StrGenerator().gen(schema))
