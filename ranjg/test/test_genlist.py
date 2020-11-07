import unittest
import jsonschema
from ranjg import genlist
from ranjg.error import SchemaConflictError, InvalidSchemaError


class TestGenlist(unittest.TestCase):
    """Test class of ``genlist``

    Test ``ranjg.genlist``
    """

    # TODO: 仕様の再編とテスト内容の全面見直し。

    def test_genlist_with_empty_schema(self):
        """ Normalized System Test

        ``genlist(schema)`` returns a list even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``genlist(schema)`` returns ``list`` value.
        """
        schema = {}
        generated = genlist(schema)
        self.assertIsInstance(generated, list)
        jsonschema.validate(generated, schema)

    def test_genlist_with_minItems(self):
        """ Normalized System Test

        ``genlist(schema)`` returns a list. When ``schema.minItems`` is specified, the result list has at least
        ``minItems`` elements.

        assert that:
            When ``schema.minItems`` is specified, the result list has at least ``minItems`` elements.
        """
        threshold_list = (0, 1.0, 30.0, 100, 300)

        for min_items in threshold_list:
            with self.subTest(min_items=min_items):
                schema = {
                    "minItems": min_items
                }
                generated = genlist(schema)
                self.assertIsInstance(generated, list)
                self.assertGreaterEqual(len(generated), min_items)
                jsonschema.validate(generated, schema)

    def test_genlist_with_maxItems(self):
        """ Normalized System Test

        ``genlist(schema)`` returns a list. When ``schema.maxItems`` is specified, the result list has at most
        ``maxItems`` elements.

        assert that:
            When ``schema.maxItems`` is specified, the result list has at most ``maxItems`` elements.
        """
        threshold_list = (0, 1.0, 30.0, 100, 300)

        for max_items in threshold_list:
            with self.subTest(max_items=max_items):
                schema = {
                    "maxItems": max_items
                }
                generated = genlist(schema)
                self.assertIsInstance(generated, list)
                self.assertLessEqual(len(generated), max_items)
                jsonschema.validate(generated, schema)

    def test_genlist_with_negative_minItems(self):
        """ Semi-normalized System Test

        ``schema.minItems`` must be non-negative. When ``schema.minItems < 0``, ``genlist(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.minItems < 0``, ``genlist(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minItems": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: genlist(schema))

    def test_genlist_with_negative_maxItems(self):
        """ Semi-normalized System Test

        ``schema.maxItems`` must be non-negative. When ``schema.maxItems < 0``, ``genlist(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.maxItems < 0``, ``genlist(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxItems": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: genlist(schema))

    def test_genlist_with_non_integer_minItems(self):
        """ Semi-normalized System Test

        ``schema.minItems`` must be integer. More precisely, ``minItems`` must be a number value divided by 1. When
        ``schema.minItems`` cannot divided by 1, ``genlist(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.minItems`` cannot divided by 1, ``genlist(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minItems": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: genlist(schema))

    def test_genlist_with_non_integer_maxItems(self):
        """ Semi-normalized System Test

        ``schema.maxItems`` must be integer. More precisely, ``maxItems`` must be a number value divided by 1. When
        ``schema.maxItems`` cannot divided by 1, ``genlist(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.maxItems`` cannot divided by 1, ``genlist(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxItems": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: genlist(schema))

    def test_genlist_with_tight_length(self):
        """ Normalized System Test

        When ``schema.minItems`` and ``schema.maxItems`` specified, ``genlist(schema)`` returns a list of length in
        range [``schema.minItems``, ``schema.maxItems``]. So when ``minItems`` value equals ``maxItems`` value, the
        length of returned list equals them.

        assert that:
            When ``schema.minItems`` equals ``schema.maxItems``, ``getlist(schema)`` returns a list of length
            ``minItems``.
        """
        threshold_list = (0, 1, 30, 100.0, 300.0)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "type": "array",
                    "minItems": threshold,
                    "maxItems": threshold,
                }
                generated = genlist(schema)
                self.assertEqual(len(generated), threshold)
                jsonschema.validate(generated, schema)

    def test_genlist_with_single_items(self):
        """ Normalized System Test

        When ``schema.items`` is specified with dict, elements in the returned list are valid by the dict as schema.

        assert that:
            When ``schema.minItems > 0`` and ``schema.items`` is dict has ``type``, then elements in the returned list
            is type of the ``type``.
        """
        type_list = (("string", str),
                     ("number", float),
                     ("integer", int),
                     ("boolean", bool),
                     ("array", list),
                     ("object", dict))

        for type_name, type_cls in type_list:
            with self.subTest(type_name=type_name, type_cls=type_cls):
                schema = {
                    "type": "array",
                    "minItems": 5,
                    "items": {
                        "type": type_name,
                    }
                }
                generated = genlist(schema)
                self.assertGreater(len(generated), 0)
                for item in generated:
                    self.assertIsInstance(item, type_cls)
                jsonschema.validate(generated, schema)

    def test_genlist_with_tuple_items(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas, each element in the returned list is valid by each
        schema in list.
        And when ``schema.additionalItems`` is not specified, the returned list is length of equal to it of ``items``
        (no additional items are generated).

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
        """
        schema = {
            "type": "array",
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        # TODO: 複数のタイプと長さを使って試験する。
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        jsonschema.validate(generated, schema)

    def test_genlist_with_tuple_items_and_tight_length(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas and ``schema.additionalItems`` is ``True``,
        the generated list has ``n`` items; ``n`` abide by ``schema.minItems`` and ``schema.maxItems``.

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
            When ``schema.additionalItems`` is ``True`` and ``schema.minItems == schema.maxItems``, the result list is
            length of ``minItems``.
        """
        schema = {
            "type": "array",
            "additionalItems": True,
            "minItems": 5,
            "maxItems": 5,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 5)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        jsonschema.validate(generated, schema)

    # TODO: additionalItems を指定せず、minItems を len(items) より大きくするテスト (additionalItems が False であるときと同じ動作)

    def test_genlist_with_tuple_items_and_tight_length_and_additional_schema(self):
        schema = {
            "type": "array",
            "additionalItems": {"type": "boolean"},
            "minItems": 5,
            "maxItems": 5,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 5)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        self.assertIsInstance(generated[3], bool)
        self.assertIsInstance(generated[4], bool)
        jsonschema.validate(generated, schema)

    def test_genlist_with_tuple_items_and_same_size_maxItems(self):
        schema = {
            "type": "array",
            "maxItems": 3,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        jsonschema.validate(generated, schema)

    def test_genlist_with_tuple_items_and_same_size_maxItems_and_additional_schema(self):
        schema = {
            "type": "array",
            "maxItems": 3,
            "additionalItems": {"type": "boolean"},
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        jsonschema.validate(generated, schema)

    def test_genlist_with_tuple_items_and_same_size_maxItems_and_additional_true(self):
        schema = {
            "type": "array",
            "maxItems": 3,
            "additionalItems": True,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        jsonschema.validate(generated, schema)

    def test_genlist_with_tuple_items_and_too_less_maxItems(self):
        schema = {
            "type": "array",
            "maxItems": 2,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        self.assertRaises(SchemaConflictError, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_less_maxItems_and_additional_schema(self):
        schema = {
            "type": "array",
            "additionalItems": {"type": "boolean"},
            "maxItems": 2,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        self.assertRaises(SchemaConflictError, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_less_maxItems_and_additional_true(self):
        schema = {
            "type": "array",
            "additionalItems": True,
            "maxItems": 2,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        self.assertRaises(SchemaConflictError, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_less_maxItems_and_additional_false(self):
        schema = {
            "type": "array",
            "additionalItems": False,
            "maxItems": 2,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        self.assertRaises(SchemaConflictError, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_great_minItems_and_additional_false(self):
        schema = {
            "type": "array",
            "additionalItems": False,
            "minItems": 4,
            "items": [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ]
        }
        self.assertRaises(SchemaConflictError, lambda: genlist(schema))
