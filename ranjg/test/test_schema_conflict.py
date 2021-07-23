import unittest

from ranjg import gen
from ranjg.error import SchemaConflictError


class TestSchemaConflictError(unittest.TestCase):
    """Test class of ``SchemaConflictError``

    Test ``SchemaConflictError``
    """

    def test_conflict_root_str(self):
        """ Semi-normalized System Test
        """
        schema_list = (
            {"type": "string", "minLength": 10, "maxLength": 5},
        )

        for schema in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaises(SchemaConflictError) as cm:
                    gen(schema)
                self.assertTupleEqual(cm.exception.context.key_path, tuple())

    def test_conflict_root_int(self):
        """ Semi-normalized System Test
        """
        schema_list = (
            {"type": "integer", "minimum": 10, "maximum": 5},
        )

        for schema in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaises(SchemaConflictError) as cm:
                    gen(schema)
                self.assertTupleEqual(cm.exception.context.key_path, tuple())

    def test_conflict_root_num(self):
        """ Semi-normalized System Test
        """
        schema_list = (
            {"type": "number", "minimum": 10, "maximum": 5},
        )

        for schema in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaises(SchemaConflictError) as cm:
                    gen(schema)
                self.assertTupleEqual(cm.exception.context.key_path, tuple())

    def test_conflict_root_list(self):
        """ Semi-normalized System Test
        """
        schema_list = (
            {"type": "array", "minItems": 10, "maxItems": 5, "items": {"type": "null"}},
        )

        for schema in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaises(SchemaConflictError) as cm:
                    gen(schema)
                self.assertTupleEqual(cm.exception.context.key_path, tuple())

    def test_conflict_context(self):
        """ Semi-normalized System Test
        """
        schema_list = (
            ({"type": "array",
              "minItems": 2,
              "items": [{}, {"type": "number", "minimum": 10, "maximum": 5}]}, (1,)),
            ({"type": "array",
              "minItems": 3,
              "items": [{}, {}, {"type": "number", "minimum": 10, "maximum": 5}, {}]}, (2,)),
            ({"type": "object",
              "properties": {"conflict": {"type": "number", "minimum": 10, "maximum": 5}},
              "required": ["conflict"]}, ("conflict",)),
            ({"type": "object",
              "properties": {"list": {"type": "array",
                                      "minItems": 3,
                                      "items": [{}, {"type": "number", "minimum": 10, "maximum": 5}, {}]}},
              "required": ["list"]}, ("list", 1)),
        )

        for schema, path in schema_list:
            with self.subTest(schema=schema):
                with self.assertRaises(SchemaConflictError) as cm:
                    gen(schema)
                self.assertTupleEqual(cm.exception.context.key_path, path)
