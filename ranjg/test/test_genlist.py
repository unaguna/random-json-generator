import unittest
import jsonschema
from ranjg import genlist
from ranjg.error import SchemaConflictError


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

    # TODO: minItems だけ指定するテスト (0を含む)
    # TODO: maxItems だけ指定するテスト (0を含む)
    # TODO: 負の minItems だけ指定するテスト
    # TODO: 負の maxItems だけ指定するテスト

    def test_genlist_with_tight_length(self):
        """ Normalized System Test

        When ``schema.minItems`` and ``schema.maxItems`` specified, ``genlist(schema)`` returns a list of length in
        range [``schema.minItems``, ``schema.maxItems``]. So when ``minItems`` value equals ``maxItems`` value, the
        length of returned list equals them.

        assert that:
            When ``schema.minItems`` equals ``schema.maxItems``, ``getlist(schema)`` returns a list of length
            ``minItems``.
        """
        # TODO: 複数の値を使って試験する。 (0を含む)
        schema = {
            "type": "array",
            "minItems": 6,
            "maxItems": 6,
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 6)
        jsonschema.validate(generated, schema)

    def test_genlist_with_single_items(self):
        """ Normalized System Test

        When ``schema.items`` is specified with dict, elements in the returned list are valid by the dict as schema.

        assert that:
            When ``schema.minItems > 0`` and ``schema.items`` is dict has ``type``, then elements in the returned list
            is type of the ``type``.
        """
        schema = {
            "type": "array",
            "minItems": 5,
            "items": {
                "type": "string",
            }
        }
        # TODO: 複数のタイプを使って試験する。
        # TODO: 生成されたリストが要素を持つことも確かめる
        generated = genlist(schema)
        for item in generated:
            self.assertIsInstance(item, str)
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
