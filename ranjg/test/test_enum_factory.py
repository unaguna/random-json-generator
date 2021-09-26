import unittest
from typing import Sequence, Dict

from ranjg import Options
from ranjg.error import SchemaConflictError
from ranjg.factories import EnumFactory


class TestEnumFactory(unittest.TestCase):
    """Test class of ``EnumFactory``

    Test ``EnumFactory``
    """

    def test_gen(self):
        """ Normalized System Test
        """
        case_list = (
            (['1', 2.0, 1.5], {}, {'1', 2.0, 1.5}),
            (['1', 2.0, 1.5], {'type': 'integer'}, {2.0}),
            (['1', 2.0, 1.5], {'maximum': 1.9}, {'1', 1.5}),
            ([['a', 'b'], {'a': 'b'}], {}, [('list', 'a', 'b'), ('dict', ('a', 'b'))]),
        )

        for enum, schema, expected_set in case_list:
            schema['enum'] = enum
            with self.subTest(expected=expected_set):
                # でた値を保管。後で数える
                result_set = set()

                factory = EnumFactory(schema)

                # 確率的事象につき複数回行う
                for _ in range(20):
                    generated = factory.gen()
                    if isinstance(generated, list):
                        result_set.add(('list', *generated))
                    elif isinstance(generated, dict):
                        result_set.add(('dict', *generated.items()))
                    else:
                        result_set.add(generated)

                self.assertGreaterEqual(len(result_set), min(len(expected_set), 2))
                for value in result_set:
                    self.assertIn(value, expected_set)

    def test_gen_return_copied_object(self):
        """ Normalized System Test

        The returned value equals to one of values in schema.enum but not same object.
        """
        result_list = (
            [[1], 2],
            {'a': {'b': 'c'}},
        )

        for result in result_list:
            schema = {'enum': [result]}
            with self.subTest(result=result):
                actual = EnumFactory(schema).gen()

                self.assertEqual(actual, result)
                self.assertIsNot(actual, result)

                if isinstance(actual, Sequence):
                    self.assertIsNot(actual[0], result[0])
                elif isinstance(actual, Dict):
                    self.assertIsNot(actual['a'], result['a'])
                else:
                    assert False

    def test_init_with_empty_enum(self):
        """ Semi-normalized System Test

        ``EnumFactory(schema)`` raises error if ``schema.enum`` is empty sequence.
        """
        schema = {'enum': []}

        with self.assertRaisesRegex(SchemaConflictError,
                                    "schema.enum must contain at least 1 value"):
            EnumFactory(schema)

    def test_init_with_enum_conflicts_other_schema_conditions(self):
        """ Semi-normalized System Test

        ``EnumFactory(schema)`` raises error if no values in ``schema.enum`` satisfy the schema.
        """
        schema_list = (
            {'enum': [1, '1'], 'type': 'boolean'},
            {'enum': [1, '1'], 'maximum': 0, 'minLength': 2},
            {'enum': ['1', '2'], 'pattern': 'a'},
        )

        for schema in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaisesRegex(SchemaConflictError,
                                            "At least 1 value of schema.enum must satisfy the schema"):
                    EnumFactory(schema)

    def test_init_without_enum_schema(self):
        """ Semi-normalized System Test

        ``EnumFactory(schema)`` raises error if ``schema.enum`` is not sequence.
        """
        schema_list = (
            {'type': 'integer'},
            {'enum': None},
            {'enum': 5},
        )

        for schema in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaisesRegex(ValueError,
                                            "schema for EnumFactory must have an array 'enum'"):
                    EnumFactory(schema)

    def test_gen_with_option_no_copy(self):
        """ Normalized System Test

        If ``options.enum_copy_style == 'NO_COPY'``, generated value has same id with one of ``schema.enum``.
        """
        result_list = (
            [1, 2],
            {'a': 'b'},
        )

        for result in result_list:
            schema = {'enum': [result]}
            with self.subTest(result=result):
                actual = EnumFactory(schema).gen(options=Options(enum_copy_style='NO_COPY'))

                self.assertEqual(actual, result)
                self.assertIs(actual, result)

    def test_gen_with_option_shallow_copy(self):
        """ Normalized System Test

        If ``options.enum_copy_style == 'SHALLOW_COPY'``, generated value is shallow copy of one of ``schema.enum``.
        """
        result_list = (
            [[1], 2],
            {'a': {'b': 'c'}},
        )

        for result in result_list:
            schema = {'enum': [result]}
            with self.subTest(result=result):
                actual = EnumFactory(schema).gen(options=Options(enum_copy_style='SHALLOW_COPY'))

                self.assertEqual(actual, result)
                self.assertIsNot(actual, result)

                if isinstance(actual, Sequence):
                    self.assertIs(actual[0], result[0])
                elif isinstance(actual, Dict):
                    self.assertIs(actual['a'], result['a'])
                else:
                    assert False

    def test_gen_with_option_deep_copy(self):
        """ Normalized System Test

        If ``options.enum_copy_style == 'DEEP_COPY'``, generated value is deep copy of one of ``schema.enum``.
        """
        result_list = (
            [[1], 2],
            {'a': {'b': 'c'}},
        )

        for result in result_list:
            schema = {'enum': [result]}
            with self.subTest(result=result):
                actual = EnumFactory(schema).gen(options=Options(enum_copy_style='DEEP_COPY'))

                self.assertEqual(actual, result)
                self.assertIsNot(actual, result)

                if isinstance(actual, Sequence):
                    self.assertIsNot(actual[0], result[0])
                elif isinstance(actual, Dict):
                    self.assertIsNot(actual['a'], result['a'])
                else:
                    assert False
