import unittest

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
            ([['a', 'b'], {'a': 'b'}], {}, [['a', 'b'], {'a': 'b'}]),
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
                    result_set.add(generated)

                self.assertGreaterEqual(len(result_set), 2)
                for value in result_set:
                    self.assertIn(value, expected_set)

    def test_init_with_empty_enum(self):
        """ Semi-normalized System Test

        ``EnumFactory(schema)`` raises error if ``schema.enum`` is empty Iterable.
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
