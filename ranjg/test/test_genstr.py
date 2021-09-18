import unittest
from unittest import mock

import jsonschema
from ranjg import genstr, Options
from .._context import GenerationContext
from ..factory import StrFactory
from ranjg.error import InvalidSchemaError, SchemaConflictError, GenerateConflictError


class TestGenstr(unittest.TestCase):
    """Test class of ``genstr``

    Test ``ranjg.genstr``
    """

    def test_when_gennum_then_call_init(self):
        """ Normalized System Test

        ``genstr()`` is wrapper of ``StrFactory#gen()``.

        assert that:
            When ``genstr`` is called, then ``StrFactory()`` runs.
        """
        _context_dummy = GenerationContext.root({}).resolve('key', {})
        _options_dummy = Options.default()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "string"}, None, False, None),
            ({"type": "string"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with self.subTest(schema=schema, is_validated=is_validated, options=(options is not None)), \
                    mock.patch('ranjg.factory.StrFactory.__init__', return_value=None) as mock_gen, \
                    mock.patch('ranjg.factory.StrFactory.gen'):
                genstr(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(schema, schema_is_validated=is_validated)

    def test_when_gennum_then_call_gen(self):
        """ Normalized System Test

        ``genstr()`` is wrapper of ``StrFactory#gen()``.

        assert that:
            When ``genstr`` is called, then ``StrFactory#gen()`` runs.
        """
        _context_dummy = GenerationContext.root({}).resolve('key', {})
        _options_dummy = Options.default()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "string"}, None, False, None),
            ({"type": "string"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with self.subTest(schema=schema, is_validated=is_validated, options=(options is not None)), \
                    mock.patch('ranjg.factory.StrFactory.gen') as mock_gen:
                genstr(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(context=context, options=options)


class TestStrFactory(unittest.TestCase):
    """Test class of ``StrFactory``

    Test ``StrFactory``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``StrFactory(schema).gen()`` returns a string value. When ``schema`` is empty, the result contains only
        alphabets.

        assert that:
            When the schema is empty, ``StrFactory(schema).gen()`` returns ``str`` value contains only alphabets.
        """
        schema = {}
        generated = StrFactory(schema).gen()
        self.assertIsInstance(generated, str)
        self.assertTrue(generated.isalpha())
        jsonschema.validate(generated, schema)

    def test_gen_with_maxLength_0(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``StrFactory(schema).gen()`` returns a string value with a length of
        ``maxLength`` or less.

        assert that:
            When ``schema.maxLength == 0``, ``StrFactory(schema).gen()`` returns the empty string.
        """
        schema = {"maxLength": 0}
        generated = StrFactory(schema).gen()
        self.assertEqual(generated, "")
        jsonschema.validate(generated, schema)

    def test_gen_with_maxLength(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``StrFactory(schema).gen()`` returns a string value with a length of
        ``maxLength`` or less.

        assert that:
            When ``schema.maxLength``, ``StrFactory(schema).gen()`` returns a string with a length of ``maxLength`` or
            less.
        """
        threshold_list = (1, 2, 3, 1.0)

        for max_length in threshold_list:
            with self.subTest(max_length=max_length):
                schema = {"maxLength": max_length}
                generated = StrFactory(schema).gen()
                self.assertIsInstance(generated, str)
                self.assertLessEqual(len(generated), max_length)
                jsonschema.validate(generated, schema)

    def test_gen_with_negative_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be non-negative. When ``schema.maxLength < 0``, ``StrFactory(schema).gen()`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.maxLength < 0``, ``StrFactory(schema).gen()`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": -1
        }
        with self.assertRaisesRegex(InvalidSchemaError,
                                    fr'On instance\["maxLength"\]:\s+'
                                    fr'{schema.get("maxLength")} is less than the minimum of 0'):
            StrFactory(schema).gen()

    def test_gen_with_non_integer_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be integer. More precisely, ``maxLength`` must be a number value divided by 1. When
        ``schema.maxLength`` cannot divided by 1, ``StrFactory(schema).gen()`` raises InvalidSchemaError.

        assert that:
            When ``schema.maxLength`` cannot divided by 1, ``StrFactory(schema).gen()`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": 1.1
        }
        with self.assertRaisesRegex(InvalidSchemaError,
                                    fr'On instance\["maxLength"\]:\s+'
                                    fr'{schema.get("maxLength")} is not a multiple of 1'):
            StrFactory(schema).gen()

    def test_gen_with_non_number_maxLength(self):
        """ Semi-normalized System Test

        ``schema.maxLength`` must be number. When ``schema.maxLength`` isn't number, ``StrFactory(schema).gen()``
        raises InvalidSchemaError.

        assert that:
            When ``schema.maxLength`` isn't number, ``StrFactory(schema).gen()`` raises InvalidSchemaError.
        """
        schema = {
            "maxLength": "1"
        }
        with self.assertRaisesRegex(InvalidSchemaError,
                                    fr'On instance\["maxLength"\]:\s+'
                                    fr'{repr(schema.get("maxLength"))} is not of type \'number\''):
            StrFactory(schema).gen()

    def test_gen_with_minLength(self):
        """ Normalized System Test

        When ``schema.minLength`` is specified, ``StrFactory(schema).gen()`` returns a string value with a length of
        ``minLength`` or more.

        assert that:
            When ``schema.minLength`` is specified, ``StrFactory(schema).gen()`` returns the string value and it's
            length is greater than or equal to ``minLength``.
        """
        threshold_list = (1, 2, 3, 1.0)

        for min_length in threshold_list:
            with self.subTest(min_length=min_length):
                schema = {"minLength": min_length}
                generated = StrFactory(schema).gen()
                self.assertIsInstance(generated, str)
                self.assertGreaterEqual(len(generated), min_length)
                jsonschema.validate(generated, schema)

    def test_gen_with_negative_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be non-negative. When ``schema.minLength < 0``, ``StrFactory(schema).gen()`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.minLength < 0``, ``StrFactory(schema).gen()`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": -1
        }
        with self.assertRaisesRegex(InvalidSchemaError,
                                    fr'On instance\["minLength"\]:\s+'
                                    fr'{schema.get("minLength")} is less than the minimum of 0'):
            StrFactory(schema).gen()

    def test_gen_with_non_integer_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be integer. More precisely, ``minLength`` must be a number value divided by 1. When
        ``schema.minLength`` cannot divided by 1, ``StrFactory(schema).gen()`` raises InvalidSchemaError.

        assert that:
            When ``schema.minLength`` cannot divided by 1, ``StrFactory(schema).gen()`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": 1.1
        }
        with self.assertRaisesRegex(InvalidSchemaError,
                                    fr'On instance\["minLength"\]:\s+'
                                    fr'{schema.get("minLength")} is not a multiple of 1'):
            StrFactory(schema).gen()

    def test_gen_with_non_number_minLength(self):
        """ Semi-normalized System Test

        ``schema.minLength`` must be number. When ``schema.minLength`` isn't number, ``StrFactory(schema).gen()``
        raises InvalidSchemaError.

        assert that:
            When ``schema.minLength`` isn't number, ``StrFactory(schema).gen()`` raises InvalidSchemaError.
        """
        schema = {
            "minLength": "1"
        }
        with self.assertRaisesRegex(InvalidSchemaError,
                                    fr'On instance\["minLength"\]:\s+'
                                    fr'{repr(schema.get("minLength"))} is not of type \'number\''):
            StrFactory(schema).gen()

    def test_gen_with_length(self):
        """ Normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``StrFactory(schema).gen()`` returns a string
        value with a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when ``minLength`` and
        ``maxLength`` have same value, the length of the result equals them.

        assert that:
            When ``schema.minLength`` and ``schema.maxLength`` is specified, ``StrFactory(schema).gen()`` returns the
            string with a length ``x`` satisfies ``minLength <= x <= maxLength``.
        """
        thresholds_list = ((0, 1),
                           (10, 10),
                           (12, 15))

        for min_length, max_length in thresholds_list:
            with self.subTest(min_length=min_length, max_length=max_length):
                schema = {"minLength": min_length, "maxLength": max_length}
                generated = StrFactory(schema).gen()
                self.assertIsInstance(generated, str)
                self.assertGreaterEqual(len(generated), min_length)
                self.assertLessEqual(len(generated), max_length)
                jsonschema.validate(generated, schema)

    def test_gen_with_conflicting_length(self):
        """ Semi-normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``StrFactory(schema).gen()`` returns a string
        value with a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when
        ``minLength > maxLength``, ``StrFactory(schema).gen()`` raises SchemaConflictError.

        assert that:
            When ``schema.minLength > schema.maxLength``, ``StrFactory(schema).gen()`` raises SchemaConflictError.
        """
        thresholds_list = ((0, 1),
                           (12, 15))

        for max_length, min_length in thresholds_list:
            with self.subTest(min_length=min_length, max_length=max_length):
                schema = {"minLength": min_length, "maxLength": max_length}
                with self.assertRaisesRegex(SchemaConflictError,
                                            '"minLength" must be lower than or equal to the "maxLength" value'):
                    StrFactory(schema).gen()

    def test_gen_with_pattern(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression.

        assert that:
            When ``schema.pattern`` is valid as regular expression, ``StrFactory(schema).gen()`` returns a string
            satisfies this regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z]+\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern}
                generated = StrFactory(schema).gen()
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                jsonschema.validate(generated, schema)

    def test_gen_with_pattern_and_minLength(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression even if it
        contradicts ``schema.minLength``.

        assert that:
            When ``schema.pattern`` is valid as regular expression and ``schema.minLength`` contradicts ``pattern``,
            ``StrFactory(schema).gen()`` returns a string satisfies this regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z][A-Z]\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern, "minLength": 13}
                generated = StrFactory(schema).gen()
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                with self.assertRaisesRegex(jsonschema.ValidationError, "Failed validating 'minLength'"):
                    jsonschema.validate(generated, schema)

    def test_gen_with_pattern_and_maxLength(self):
        """ Normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression even if it
        contradicts ``schema.maxLength``.

        assert that:
            When ``schema.pattern`` is valid as regular expression and ``schema.maxLength`` contradicts ``pattern``,
            ``StrFactory(schema).gen()`` returns a string satisfies this regular expression.
        """
        pattern_list = ("\\d\\d\\d-\\d\\d\\d\\d-\\d\\d\\d",
                        "[a-z][A-Z]\\d\\d")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern, "maxLength": 3}
                generated = StrFactory(schema).gen()
                self.assertIsInstance(generated, str)
                self.assertRegex(generated, pattern)
                with self.assertRaisesRegex(jsonschema.ValidationError, "Failed validating 'maxLength'"):
                    jsonschema.validate(generated, schema)

    def test_gen_with_illegal_pattern(self):
        """ Semi-normalized System Test

        When ``schema.pattern`` is specified, the return value satisfies this as regular expression. As a result,
        when ``schema.pattern`` is invalid as regular expression, ``StrFactory(schema).gen()`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.pattern`` is invalid as regular expression, ``StrFactory(schema).gen()`` raises
            InvalidSchemaError.
        """
        pattern_list = ("[0-1",
                        "\\")

        for pattern in pattern_list:
            with self.subTest(pattern=pattern):
                schema = {"pattern": pattern}
                with self.assertRaisesRegex(InvalidSchemaError, "is not a 'regex'"):
                    StrFactory(schema).gen()


class TestOptionDefaultLength(unittest.TestCase):

    def test_default_length_with_schema_min_max(self):
        """ Normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` are specified, ``options.default_min_length_of_string``,
        ``options.default_max_length_of_string`` and ``options.default_length_range_of_genstr`` are ignored.

        assert that:
            Generated string is satisfies ``schema.minLength`` and ``schema.maxLength`` even if
            ``options.default_min_length_of_string``, ``options.default_max_length_of_string`` and
            ``options.default_length_range_of_genstr`` are specified.
        """
        options_list = (Options(),
                        Options(default_min_length_of_string=10),
                        Options(default_max_length_of_string=100),
                        Options(default_min_length_of_string=10, default_max_length_of_string=100),
                        Options(default_length_range_of_genstr=100),
                        Options(default_min_length_of_string=10, default_length_range_of_genstr=100),
                        Options(default_max_length_of_string=100, default_length_range_of_genstr=100),
                        Options(default_min_length_of_string=10, default_max_length_of_string=100,
                                default_length_range_of_genstr=100),)

        str_length = 20
        schema = {"type": "string", "minLength": str_length, "maxLength": str_length}

        for options in options_list:
            with self.subTest(min=options.default_min_length_of_string, max=options.default_max_length_of_string,
                              len=options.default_length_range_of_genstr):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(str_length, len(generated))

    def test_default_length_with_schema_min_without_schema_max(self):
        """ Normalized System Test

        When ``schema.minLength`` is specified and ``schema.maxLength`` is not, the maximum length is defined as
        ``schema.minLength`` + ``options.default_length_range_of_genstr``.
        ``options.default_min_length_of_string`` and ``options.default_max_length_of_string`` are ignored.

        assert that:
            Generated string has length between ``schema.minLength`` and ``schema.minLength`` +
            ``options.default_length_range_of_genstr``.
        """
        options_list = (Options(default_length_range_of_genstr=0),
                        Options(default_min_length_of_string=10, default_length_range_of_genstr=0),
                        Options(default_max_length_of_string=100, default_length_range_of_genstr=0),
                        Options(default_min_length_of_string=10, default_max_length_of_string=100,
                                default_length_range_of_genstr=0),)

        min_length = 20
        schema = {"type": "string", "minLength": min_length}

        for options in options_list:
            with self.subTest(min=options.default_min_length_of_string, max=options.default_max_length_of_string,
                              len=options.default_length_range_of_genstr):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(min_length, len(generated))

    def test_default_length_with_schema_max_without_schema_min(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified and ``schema.minLength`` is not, the minimum length is defined as
        ``schema.maxLength`` - ``options.default_length_range_of_genstr``.
        ``options.default_min_length_of_string`` and ``options.default_max_length_of_string`` are ignored.

        assert that:
            Generated string has length between ``schema.maxLength`` - ``options.default_length_range_of_genstr`` and
            ``schema.maxLength``.
        """
        options_list = (Options(default_length_range_of_genstr=0),
                        Options(default_min_length_of_string=10, default_length_range_of_genstr=0),
                        Options(default_max_length_of_string=100, default_length_range_of_genstr=0),
                        Options(default_min_length_of_string=10, default_max_length_of_string=100,
                                default_length_range_of_genstr=0),)

        max_length = 20
        schema = {"type": "string", "maxLength": max_length}

        for options in options_list:
            with self.subTest(min=options.default_min_length_of_string, max=options.default_max_length_of_string,
                              len=options.default_length_range_of_genstr):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(max_length, len(generated))

    def test_default_length_without_schema_min_max(self):
        """ Normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` are not specified, ``options.default_min_length_of_string``
        and ``options.default_max_length_of_string`` are used instead.
        ``options.default_length_range_of_genstr`` is ignored.

        assert that:
            Generated string is satisfies ``options.default_min_length_of_string`` and
            `options.default_max_length_of_string`` if ``schema.minLength`` and ``schema.maxLength`` are not specified.
        """
        str_length = 10
        options_list = (Options(default_min_length_of_string=str_length, default_max_length_of_string=str_length),
                        Options(default_min_length_of_string=str_length, default_max_length_of_string=str_length,
                                default_length_range_of_genstr=100),)

        schema = {"type": "string"}

        for options in options_list:
            with self.subTest(min=options.default_min_length_of_string, max=options.default_max_length_of_string,
                              len=options.default_length_range_of_genstr):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(str_length, len(generated))

    def test_negative_default_length_range(self):
        """ Semi-normalized System Test

        When ``options.default_length_range_of_genstr`` is negative, it is corrected to 0.

        assert that:
            Generated string has length of ``schema.minLength`` if ``schema.maxLength`` is not specified and
            ``options.default_length_range_of_genstr`` is negative.
            Generated string has length of ``schema.maxLength`` if ``schema.minLength`` is not specified and
            ``options.default_length_range_of_genstr`` is negative.
        """
        options_list = (Options(default_length_range_of_genstr=-1),
                        Options(default_min_length_of_string=10, default_length_range_of_genstr=-2),
                        Options(default_max_length_of_string=100, default_length_range_of_genstr=-3),
                        Options(default_min_length_of_string=10, default_max_length_of_string=100,
                                default_length_range_of_genstr=-4),)

        str_length = 20
        schema = {"type": "string", "minLength": str_length}

        for options in options_list:
            with self.subTest(target='minLength',
                              min=options.default_min_length_of_string, max=options.default_max_length_of_string,
                              len=options.default_length_range_of_genstr):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(str_length, len(generated))

        schema = {"type": "string", "maxLength": str_length}

        for options in options_list:
            with self.subTest(target='maxLength',
                              min=options.default_min_length_of_string, max=options.default_max_length_of_string,
                              len=options.default_length_range_of_genstr):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(str_length, len(generated))

    def test_reversed_default_length(self):
        """ Semi-normalized System Test

        When ``options.default_min_length_of_string`` is greater than ``options.default_max_length_of_string`` and
        they are used, SchemaConflictError is raised.
        """
        options_list = (Options(default_min_length_of_string=10, default_max_length_of_string=9),
                        Options(default_min_length_of_string=11, default_max_length_of_string=10,
                                default_length_range_of_genstr=-4),
                        Options(default_min_length_of_string=-1, default_max_length_of_string=-2),
                        # 負の default_min_length_of_string は 0 として扱われるので、以下の例もmin>maxとして処理する。
                        Options(default_min_length_of_string=-2, default_max_length_of_string=-1),)

        schema = {"type": "string"}

        for options in options_list:
            with self.subTest(default_min_length_of_string=options.default_min_length_of_string):
                with self.assertRaisesRegex(GenerateConflictError,
                                            '"options.default_min_length_of_string" must be lower than or equal to '
                                            'the "options.default_max_length_of_string" value'):
                    StrFactory(schema).gen(options=options)

    def test_negative_default_min_length(self):
        """ Semi-normalized System Test

        When ``options.default_min_length_of_string`` is negative, it is corrected to 0.
        """
        options_list = (Options(default_min_length_of_string=-3, default_max_length_of_string=0),
                        Options(default_min_length_of_string=-4, default_max_length_of_string=0,
                                default_length_range_of_genstr=0),)

        schema = {"type": "string"}

        for options in options_list:
            with self.subTest(default_min_length_of_string=options.default_min_length_of_string):
                generated = StrFactory(schema).gen(options=options)
                self.assertEqual(0, len(generated))
