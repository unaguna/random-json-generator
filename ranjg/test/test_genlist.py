import itertools
import unittest
from unittest import mock

import jsonschema
from ranjg import genlist
from ranjg._context import Context
from .._generator import ListGenerator
from .._generator.__list import _get_range_of_length
from ranjg.error import SchemaConflictError, InvalidSchemaError


class TestGenlist(unittest.TestCase):
    """Test class of ``genlist``

    Test ``ranjg.genlist``
    """

    def test_genlist(self):
        """ Normalized System Test

        ``genlist()`` is wrapper of ``BoolGenerator#gen()``.

        assert that:
            When ``genlist`` is called, then ``BoolGenerator#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        params_list = (
            (None, None, False),
            ({"type": "array"}, None, False),
            ({"type": "array"}, None, True),
            (None, _context_dummy, False),
        )

        for schema, context, is_validated in params_list:
            with mock.patch('ranjg._generator.ListGenerator.gen') as mock_gen:
                genlist(schema, context=context, schema_is_validated=is_validated)
                mock_gen.assert_called_once_with(schema, context=context, schema_is_validated=is_validated)


class TestListGenerator(unittest.TestCase):
    """Test class of ``ListGenerator``

    Test ``ListGenerator``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``ListGenerator().gen(schema)`` returns a list even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``ListGenerator().gen(schema)`` returns ``list`` value.
        """
        schema = {}
        generated = ListGenerator().gen(schema)
        self.assertIsInstance(generated, list)
        jsonschema.validate(generated, schema)

    def test_gen_with_minItems(self):
        """ Normalized System Test

        ``ListGenerator().gen(schema)`` returns a list. When ``schema.minItems`` is specified, the result list has at
        least ``minItems`` elements.

        assert that:
            When ``schema.minItems`` is specified, the result list has at least ``minItems`` elements.
        """
        threshold_list = (0, 1.0, 30.0, 100, 300)

        for min_items in threshold_list:
            with self.subTest(min_items=min_items):
                schema = {
                    "minItems": min_items
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                self.assertGreaterEqual(len(generated), min_items)
                jsonschema.validate(generated, schema)

    def test_gen_with_maxItems(self):
        """ Normalized System Test

        ``ListGenerator().gen(schema)`` returns a list. When ``schema.maxItems`` is specified, the result list has at
        most ``maxItems`` elements.

        assert that:
            When ``schema.maxItems`` is specified, the result list has at most ``maxItems`` elements.
        """
        threshold_list = (0, 1.0, 30.0, 100, 300)

        for max_items in threshold_list:
            with self.subTest(max_items=max_items):
                schema = {
                    "maxItems": max_items
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                self.assertLessEqual(len(generated), max_items)
                jsonschema.validate(generated, schema)

    def test_gen_with_negative_minItems(self):
        """ Semi-normalized System Test

        ``schema.minItems`` must be non-negative. When ``schema.minItems < 0``, ``ListGenerator().gen(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.minItems < 0``, ``ListGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minItems": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: ListGenerator().gen(schema))

    def test_gen_with_negative_maxItems(self):
        """ Semi-normalized System Test

        ``schema.maxItems`` must be non-negative. When ``schema.maxItems < 0``, ``ListGenerator().gen(schema)`` raises
        InvalidSchemaError.

        assert that:
            When ``schema.maxItems < 0``, ``ListGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxItems": -1
        }
        self.assertRaises(InvalidSchemaError, lambda: ListGenerator().gen(schema))

    def test_gen_with_non_integer_minItems(self):
        """ Semi-normalized System Test

        ``schema.minItems`` must be integer. More precisely, ``minItems`` must be a number value divided by 1. When
        ``schema.minItems`` cannot divided by 1, ``ListGenerator().gen(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.minItems`` cannot divided by 1, ``ListGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "minItems": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: ListGenerator().gen(schema))

    def test_gen_with_non_integer_maxItems(self):
        """ Semi-normalized System Test

        ``schema.maxItems`` must be integer. More precisely, ``maxItems`` must be a number value divided by 1. When
        ``schema.maxItems`` cannot divided by 1, ``ListGenerator().gen(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.maxItems`` cannot divided by 1, ``ListGenerator().gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "maxItems": 1.1
        }
        self.assertRaises(InvalidSchemaError, lambda: ListGenerator().gen(schema))

    def test_gen_with_tight_length(self):
        """ Normalized System Test

        When ``schema.minItems`` and ``schema.maxItems`` specified, ``ListGenerator().gen(schema)`` returns a list of
        length in range [``schema.minItems``, ``schema.maxItems``]. So when ``minItems`` value equals ``maxItems``
        value, the length of returned list equals them.

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
                generated = ListGenerator().gen(schema)
                self.assertEqual(len(generated), threshold)
                jsonschema.validate(generated, schema)

    def test_gen_with_param_conflict_min_max(self):
        """ Semi-normalized System Test

        When ``schema.minItems`` and ``schema.maxItems`` specified, ``ListGenerator().gen(schema)`` returns a list of
        length in range [``schema.minItems``, ``schema.maxItems``].  As a result, when ``maximum < minimum``,
        SchemaConflictError is raised.

        assert that:
            When the schema has ``properties.minItems > properties.maxItems``, ``ListGenerator().gen(schema)`` raised
            SchemaConflictError.
        """
        thresholds_list = ((0, 10),
                           (5, 10))
        for max_items, min_items in thresholds_list:
            with self.subTest(min_items=min_items, max_items=max_items):
                schema = {
                    "minItems": min_items,
                    "maxItems": max_items,
                }
                self.assertRaises(SchemaConflictError, lambda: ListGenerator().gen(schema))

    def test_gen_with_single_items(self):
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
                generated = ListGenerator().gen(schema)
                self.assertGreater(len(generated), 0)
                for item in generated:
                    self.assertIsInstance(item, type_cls)
                jsonschema.validate(generated, schema)

    def test_gen_with_tuple_items(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas, each element in the returned list is valid by each
        schema in list. However, the length of the result is not limited by ``items``. First ``len(items)`` elements of
        the result satisfies each schema in ``items``, and others satisfies ``schema.additionalItems`` when
        ``additionalItems`` is specified with a schema object.

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
        """
        items_list = [
            [
                {"type": "string"},
                {"type": "null"},
                {"type": "integer"},
            ],
            [
                {"type": "string"},
                {"type": "integer"},
                {"type": "number"},
                {"type": "integer"},
            ],
            [
                {"type": "object"},
            ],
            [
                {"type": "array"},
            ],
        ]

        for items in items_list:
            with self.subTest(items=items):
                schema = {
                    "type": "array",
                    "minItems": 1,
                    "items": items,
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                for generated_item, schema_item in zip(generated, schema["items"]):
                    if schema_item["type"] == "null":
                        self.assertIsNone(generated_item)
                    else:
                        self.assertIsInstance(generated_item, _type_to_cls(schema_item["type"]))
                jsonschema.validate(generated, schema)

    def test_gen_with_tuple_items_and_tight_length_and_additional_true(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas, the generated list has ``n`` items; ``n`` abide by
        ``schema.minItems`` and ``schema.maxItems``. When ``schema.additionalItems`` is ``True``, it is ignored.

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
            When ``schema.additionalItems`` is ``True`` and ``schema.minItems == schema.maxItems``, the result list is
            length of ``minItems``.
        """
        threshold_list = (0, 1, 5, 10.0, 20)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "type": "array",
                    "additionalItems": True,
                    "minItems": threshold,
                    "maxItems": threshold,
                    "items": [
                        {"type": "string"},
                        {"type": "null"},
                        {"type": "integer"},
                        {"type": "integer"},
                        {"type": "number"},
                    ]
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                self.assertEqual(len(generated), threshold)
                for generated_item, schema_item in zip(generated, schema["items"]):
                    if schema_item["type"] == "null":
                        self.assertIsNone(generated_item)
                    else:
                        self.assertIsInstance(generated_item, _type_to_cls(schema_item["type"]))
                jsonschema.validate(generated, schema)

    def test_gen_with_tuple_items_and_tight_length(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas, the generated list has ``n`` items; ``n`` abide by
        ``schema.minItems`` and ``schema.maxItems``.

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
            When ``schema.additionalItems`` is not specified and ``schema.minItems`` is specified, the result list
            is length of at least ``minItems``.
        """
        threshold_list = (0, 1, 5, 10.0, 20)

        for threshold in threshold_list:
            with self.subTest(threshold=threshold):
                schema = {
                    "type": "array",
                    "minItems": threshold,
                    "maxItems": threshold,
                    "items": [
                        {"type": "string"},
                        {"type": "null"},
                        {"type": "integer"},
                        {"type": "integer"},
                        {"type": "number"},
                    ]
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                self.assertEqual(len(generated), threshold)
                for generated_item, schema_item in zip(generated, schema["items"]):
                    if schema_item["type"] == "null":
                        self.assertIsNone(generated_item)
                    else:
                        self.assertIsInstance(generated_item, _type_to_cls(schema_item["type"]))
                jsonschema.validate(generated, schema)

    def test_gen_with_tuple_items_and_tight_length_and_additional_schema(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas and ``schema.additionalItems`` is a schema object,
        the (n+1)th or more elements of the generated list satisfy the schema ``schema.additionalItems``.

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
            When ``schema.additionalItems`` is a schema object and ``schema.minItems`` is specified, the result list
            is length of at least ``minItems`` and the (n+1)th or more elements of the generated list satisfy the schema
            ``schema.additionalItems``.
        """
        additional_items_type_list = ("integer",
                                      "number",
                                      "boolean",
                                      "string",
                                      "array",
                                      "object")

        for additional_items_type in additional_items_type_list:
            with self.subTest(additional_items_type=additional_items_type):
                schema = {
                    "type": "array",
                    "additionalItems": {"type": additional_items_type},
                    "minItems": 5,
                    "items": [
                        {"type": "string"},
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                }
                generated = ListGenerator().gen(schema)
                self.assertGreaterEqual(len(generated), 5)
                self.assertIsInstance(generated[0], str)
                self.assertIsNone(generated[1])
                self.assertIsInstance(generated[2], int)
                self.assertIsInstance(generated[3], _type_to_cls(additional_items_type))
                self.assertIsInstance(generated[4], _type_to_cls(additional_items_type))
                jsonschema.validate(generated, schema)

    def test_gen_with_tuple_items_and_maxItems(self):
        """ Normalized System Test

        When ``schema.items`` is specified with a list of schemas and ``schema.maxItems`` is the length of ``items``,
        the result list has at most ``maxItems`` elements even if the length of ``schema.items`` is greater than
        ``schema.maxItems``.

        assert that:
            When ``schema.items`` is a list of dict has ``type``, then each elements in the returned list is type of
            each schema's ``type``.
            When ``schema.maxItems`` is specified, the result list has at most ``maxItems`` elements.
        """
        max_items_list = (0, 1, 5, 10.0, 20)

        for max_items in max_items_list:
            with self.subTest(max_items=max_items):
                schema = {
                    "type": "array",
                    "maxItems": max_items,
                    "items": [
                        {"type": "string"},
                        {"type": "null"},
                        {"type": "integer"},
                        {"type": "integer"},
                        {"type": "number"},
                    ]
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                self.assertLessEqual(len(generated), max_items)
                for generated_item, schema_item in zip(generated, schema["items"]):
                    if schema_item["type"] == "null":
                        self.assertIsNone(generated_item)
                    else:
                        self.assertIsInstance(generated_item, _type_to_cls(schema_item["type"]))
                jsonschema.validate(generated, schema)

    def test_gen_with_tuple_items_and_too_great_minItems_and_additional_false(self):
        """ Semi-normalized System Test

        When ``schema.minItems`` is specified, the result list must have at least ``minItems`` elements. On the other
        hand, when ``schema.items`` is specified as list and ``schema.additionalItems`` is ``false``, the result list
        must have at most the length of ``items``. As a result, when ``schema.additionalItems`` is ``false`` and
        ``len(schema.items) < schema.minItems``, ``ListGenerator().gen(schema)`` raises SchemaConflictError.

        assert that:
            When ``schema.additionalItems`` is ``false`` and ``len(schema.items) < schema.minItems``,
            ``ListGenerator().gen(schema)`` raises SchemaConflictError.
        """
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
        self.assertRaises(SchemaConflictError, lambda: ListGenerator().gen(schema))

    def test_gen_with_tuple_items_and_minItems_and_additional_false(self):
        """ Normalized System Test

        When ``schema.minItems`` is specified, the result list must have at least ``minItems`` elements. On the other
        hand, when ``schema.items`` is specified as list and ``schema.additionalItems`` is ``false``, the result list
        must have at most the length of ``items``.

        assert that:
            When ``schema.additionalItems`` is ``false`` and ``len(schema.items) >= schema.minItems``,
            the result list has at least ``minItems`` elements.
        """
        min_items_list = (0, 1, 2, 3)
        for min_items in min_items_list:
            with self.subTest(min_items=min_items):
                schema = {
                    "type": "array",
                    "additionalItems": False,
                    "minItems": min_items,
                    "items": [
                        {"type": "string"},
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                }
                generated = ListGenerator().gen(schema)
                self.assertIsInstance(generated, list)
                self.assertGreaterEqual(len(generated), min_items)


class TestGenlistLengthRange(unittest.TestCase):
    """Test class of ``__genlist._get_range_of_length``

    Test ``ranjg.__genlist._get_range_of_length``. This function returns a range of length of list to generate by
    ``genlist``.
    """

    def test_list_length_range_with_empty_schema(self):
        """ Normalized System Test

        When ``schema`` is empty, the range are not defined. Because this function returns the schema's value, it
        returns None instead of 0 if the minimum value is not specified.

        assert that:
            When ``schema`` is empty, ``_get_inclusive_integer_range(schema)`` returns ``None, None``.
        """
        schema = {}
        min_items, max_items = _get_range_of_length(schema, Context.root(schema))
        self.assertIsNone(min_items)
        self.assertIsNone(max_items)

    def test_list_length_range_with_empty_list_schema(self):
        """ Normalized System Test

        When ``schema`` is list-validation style and neither ``schema.minItems`` or ``schema.maxItems`` aren't
        specified, the range are not defined. Because this function returns the schema's value, it
        returns None instead of 0 if the minimum value is not specified.

        assert that:
            When ``schema`` has only value ``items`` as dict, ``_get_inclusive_integer_range(schema)`` returns
            ``None, None``.
        """
        items_list = ({},
                      {"type": "number"},
                      {"type": "integer"},
                      {"type": "string"},
                      {"type": "null"},
                      {"type": "boolean"},
                      {"type": "array"},
                      {"type": "object"})
        for items in items_list:
            with self.subTest(items=items):
                schema = {"items": items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertIsNone(min_items)
                self.assertIsNone(max_items)

    def test_list_length_range_with_list_schema_with_min(self):
        """ Normalized System Test

         When ``schema`` is list-validation style and ``schema.minItems`` is specified, returns this value as minItems.

        assert that:
            When ``schema.items`` is dict and ``schema.minItems`` is specified and ``schema.maxItems`` is not
            specified, ``_get_inclusive_integer_range(schema)`` returns ``minItems, None``.
        """
        items_list = ({},
                      {"type": "number"},
                      {"type": "integer"},
                      {"type": "string"},
                      {"type": "null"},
                      {"type": "boolean"},
                      {"type": "array"},
                      {"type": "object"})
        min_items_list = (0, 1, 2, 3)
        for items, schema_min_items in itertools.product(items_list, min_items_list):
            with self.subTest(items=items, min_items=schema_min_items):
                schema = {"items": items, "minItems": schema_min_items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertIsNone(max_items)

    def test_list_length_range_with_tuple_schema_with_min(self):
        """ Normalized System Test

        When ``schema`` is tuple-validation style and ``schema.minItems`` is specified, returns this value as minItems.

        assert that:
            When ``schema.items`` is list and ``schema.minItems`` is specified and ``schema.maxItems`` is not
            specified, ``_get_inclusive_integer_range(schema)`` returns ``minItems, None``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        min_items_list = (0, 1, 2, 3, 5, 10)
        for items, schema_min_items in itertools.product(items_list, min_items_list):
            with self.subTest(items=items, min_items=schema_min_items):
                schema = {"items": items, "minItems": schema_min_items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertIsNone(max_items)

    def test_list_length_range_with_tuple_schema_with_min_additional_true(self):
        """ Normalized System Test

         When ``schema`` is tuple-validation style and ``schema.minItems`` is specified, returns this value as minItems.
         Even if ``schema.additionalItems = True``, it behaves in the same way as if ``additionalItems`` had not been
         specified.

        assert that:
            Even if ``schema.additionalItems = True``, when ``schema.items`` is list and ``schema.minItems`` is
            specified and ``schema.maxItems`` is not specified, ``_get_inclusive_integer_range(schema)`` returns
            ``minItems, None``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        min_items_list = (0, 1, 2, 3, 5, 10)
        for items, schema_min_items in itertools.product(items_list, min_items_list):
            with self.subTest(items=items, min_items=schema_min_items):
                schema = {"items": items, "minItems": schema_min_items, "additionalItems": True}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertIsNone(max_items)

    def test_list_length_range_with_tuple_schema_with_min_additional_dict(self):
        """ Normalized System Test

         When ``schema`` is tuple-validation style and ``schema.minItems`` is specified, returns this value as minItems.
         Even if ``schema.additionalItems`` is dict, it behaves in the same way as if ``additionalItems`` had not been
         specified.

        assert that:
            Even if ``schema.additionalItems`` is dict, when ``schema.items`` is list and ``schema.minItems`` is
            specified and ``schema.maxItems`` is not specified, ``_get_inclusive_integer_range(schema)`` returns
            ``minItems, None``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        min_items_list = (0, 1, 2, 3, 5, 10)
        for items, schema_min_items in itertools.product(items_list, min_items_list):
            with self.subTest(items=items, min_items=schema_min_items):
                schema = {"items": items, "minItems": schema_min_items, "additionalItems": items[0]}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertIsNone(max_items)

    def test_list_length_range_with_tuple_schema_with_min_additional_false(self):
        """ Normalized System Test

         When ``schema`` is tuple-validation style and ``schema.minItems`` is specified, returns this value as minItems.
         If ``schema.additionalItems = False``, as long as the length of ``items`` is greater than or equal to
         ``minItems``, it behaves in the same way as if ``additionalItems`` had not been specified. Since no additional
         items are allowed, the maximum value is determined by the ``len(items)``.

        assert that:
            When ``schema.additionalItems = False`` and ``len(schema.items) >= schema.minItems`` is
            specified and ``schema.maxItems`` is not specified, ``_get_inclusive_integer_range(schema)`` returns
            ``minItems, len(items)``.
        """
        parameter_list = ((0, [{}]),
                          (0, [{"type": "number"}]),
                          (1, [{"type": "number"}]),
                          (0, [{"type": "integer"}, {"type": "number"}]),
                          (1, [{"type": "integer"}, {"type": "number"}]),
                          (2, [{"type": "integer"}, {"type": "number"}]))
        for schema_min_items, items in parameter_list:
            with self.subTest(items=items, min_items=schema_min_items):
                schema = {"items": items, "minItems": schema_min_items, "additionalItems": False}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertEqual(max_items, len(items))

    def test_list_length_range_with_tuple_schema_with_too_large_min_additional_false(self):
        """ Semi-normalized System Test

         When ``schema`` is tuple-validation style and ``schema.additionalItems = False``, a result of
         ``ListGenerator().gen(schema)`` cannot has elements more than ``len(schema.items)``. So if ``schema.minItem``
         is greater than the length of ``schema.items``, then SchemaConflictError is raised.

        assert that:
            When ``schema.additionalItems = False`` and ``len(schema.items) < schema.minItems``,
            ``_get_inclusive_integer_range(schema)`` raises SchemaConflictError.
        """
        parameter_list = ((2, [{}]),
                          (2, [{"type": "number"}]),
                          (3, [{"type": "number"}]),
                          (3, [{"type": "integer"}, {"type": "number"}]),
                          (4, [{"type": "integer"}, {"type": "number"}]),
                          (5, [{"type": "integer"}, {"type": "number"}]))
        for schema_min_items, items in parameter_list:
            with self.subTest(items=items, min_items=schema_min_items):
                schema = {"items": items, "minItems": schema_min_items, "additionalItems": False}
                self.assertRaises(SchemaConflictError, lambda: _get_range_of_length(schema, Context.root(schema)))

    def test_list_length_range_with_list_schema_with_max(self):
        """ Normalized System Test

         When ``schema`` is list-validation style and ``schema.maxItems`` is specified, returns this value as maxItems.

        assert that:
            When ``schema.items`` is dict and ``schema.maxItems`` is specified and ``schema.minItems`` is not
            specified, ``_get_inclusive_integer_range(schema)`` returns ``None, maxItems``.
        """
        items_list = ({},
                      {"type": "number"},
                      {"type": "integer"},
                      {"type": "string"},
                      {"type": "null"},
                      {"type": "boolean"},
                      {"type": "array"},
                      {"type": "object"})
        max_items_list = (0, 1, 2, 3)
        for items, schema_max_items in itertools.product(items_list, max_items_list):
            with self.subTest(items=items, max_items=schema_max_items):
                schema = {"items": items, "maxItems": schema_max_items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertIsNone(min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_max(self):
        """ Normalized System Test

        When ``schema`` is tuple-validation style and ``schema.maxItems`` is specified, returns this value as maxItems
        as long as ``schema.additionalItems`` is not false.

        assert that:
            When ``schema.items`` is list and ``schema.maxItems`` is specified and ``schema.minItems`` is not
            specified, ``_get_inclusive_integer_range(schema)`` returns ``None, maxItems``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        max_items_list = (0, 1, 2, 3, 5, 10)
        for items, schema_max_items in itertools.product(items_list, max_items_list):
            with self.subTest(items=items, max_items=schema_max_items):
                schema = {"items": items, "maxItems": schema_max_items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertIsNone(min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_max_additional_true(self):
        """ Normalized System Test

         When ``schema`` is tuple-validation style and ``schema.maxItems`` is specified, returns this value as maxItems
         as long as ``schema.additionalItems`` is not false. Even if ``schema.additionalItems = True``,it behaves in the
         same way as if ``additionalItems`` had not been specified.

        assert that:
            Even if ``schema.additionalItems = True``, when ``schema.items`` is list and ``schema.maxItems`` is
            specified and ``schema.minItems`` is not specified, ``_get_inclusive_integer_range(schema)`` returns
            ``None, maxItems``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        max_items_list = (0, 1, 2, 3, 5, 10)
        for items, schema_max_items in itertools.product(items_list, max_items_list):
            with self.subTest(items=items, max_items=schema_max_items):
                schema = {"items": items, "maxItems": schema_max_items, "additionalItems": True}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertIsNone(min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_max_additional_dict(self):
        """ Normalized System Test

         When ``schema`` is tuple-validation style and ``schema.maxItems`` is specified, returns this value as maxItems
         as long as ``schema.additionalItems`` is not false. Even if ``schema.additionalItems`` is dict, it behaves in
         the same way as if ``additionalItems`` had not been specified.

        assert that:
            Even if ``schema.additionalItems`` is dict, when ``schema.items`` is list and ``schema.maxItems`` is
            specified and ``schema.minItems`` is not specified, ``_get_inclusive_integer_range(schema)`` returns
            ``None, maxItems``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        max_items_list = (0, 1, 2, 3, 5, 10)
        for items, schema_max_items in itertools.product(items_list, max_items_list):
            with self.subTest(items=items, max_items=schema_max_items):
                schema = {"items": items, "maxItems": schema_max_items, "additionalItems": items[0]}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertIsNone(min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_max_additional_false(self):
        """ Normalized System Test

         When ``schema`` is tuple-validation style, ``schema.maxItems`` is specified and ``schema.additionalItems`` is
         false, returns ``min(len(items), maxItems)`` as maxItems.

        assert that:
            When ``schema.additionalItems = False`` and ``schema.maxItems`` is specified,
            ``_get_inclusive_integer_range(schema)`` returns ``None, min(len(items), maxItems)``.
        """
        parameter_list = ((0, [{"type": "number"}]),
                          (1, [{"type": "number"}]),
                          (2, [{"type": "number"}]),
                          (1, [{"type": "integer"}, {"type": "number"}]),
                          (2, [{"type": "integer"}, {"type": "number"}]),
                          (3, [{"type": "integer"}, {"type": "number"}]))
        for schema_max_items, items in parameter_list:
            with self.subTest(items=items, max_items=schema_max_items):
                schema = {"items": items, "maxItems": schema_max_items, "additionalItems": False}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, None)
                self.assertEqual(max_items, min(len(items), schema_max_items))

    def test_list_length_range_with_list_schema_with_min_max(self):
        """ Normalized System Test

         Even if both of ``schema.minItems`` and ``schema.maxItems`` are specified, they do not affect each other.

        assert that:
            When ``schema.items`` is dict and both of ``schema.minItems`` and ``schema.maxItems`` are specified,
            ``_get_inclusive_integer_range(schema)`` returns ``minItems, maxItems``.
        """
        items_list = ({},
                      {"type": "number"},
                      {"type": "integer"},
                      {"type": "string"},
                      {"type": "null"},
                      {"type": "boolean"},
                      {"type": "array"},
                      {"type": "object"})
        threshold_list = ((0, 0),
                          (0, 1),
                          (1, 1),
                          (1, 2),
                          (1, 3))
        for items, (schema_min_items, schema_max_items) in itertools.product(items_list, threshold_list):
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {"items": items, "minItems": schema_min_items, "maxItems": schema_max_items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_min_max(self):
        """ Normalized System Test

         Even if both of ``schema.minItems`` and ``schema.maxItems`` are specified, they do not affect each other.

        assert that:
            When ``schema.items`` is list and both of ``schema.minItems`` and ``schema.maxItems`` are specified,
            ``_get_inclusive_integer_range(schema)`` returns ``minItems, maxItems``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        threshold_list = ((0, 0),
                          (0, 1),
                          (1, 1),
                          (1, 2),
                          (1, 3))
        for items, (schema_min_items, schema_max_items) in itertools.product(items_list, threshold_list):
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {"items": items, "minItems": schema_min_items, "maxItems": schema_max_items}
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_conflict_min_max(self):
        """ Normalized System Test

         If ``schema.minItems > schema.maxItems``, not all conditions can be met and therefore raise an exception.

        assert that:
            When ``schema.items`` is specified and ``schema.minItems > schema.maxItems``,
            ``_get_inclusive_integer_range(schema)`` raises SchemaConflictError.
        """
        items_list = ({},
                      {"type": "number"},
                      {"type": "integer"},
                      [{"type": "string"}, {"type": "integer"}])
        threshold_list = ((1, 0),
                          (2, 0),
                          (2, 1),
                          (3, 1))
        for items, (schema_min_items, schema_max_items) in itertools.product(items_list, threshold_list):
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {"items": items, "minItems": schema_min_items, "maxItems": schema_max_items}
                self.assertRaises(SchemaConflictError, lambda: _get_range_of_length(schema, Context.root(schema)))

    def test_list_length_range_with_tuple_schema_with_min_max_additional_true(self):
        """ Normalized System Test

         If ``schema.minItems > schema.maxItems``, not all conditions can be met and therefore raise an exception.

        assert that:
            Even if ``schema.additionalItems = True``, when ``schema.items`` is list and both of ``schema.minItems`` and
            ``schema.maxItems`` are specified, ``_get_inclusive_integer_range(schema)`` returns ``minItems, maxItems``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        threshold_list = ((0, 0),
                          (0, 1),
                          (1, 1),
                          (1, 2),
                          (1, 3))
        for items, (schema_min_items, schema_max_items) in itertools.product(items_list, threshold_list):
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {
                    "items": items,
                    "minItems": schema_min_items,
                    "maxItems": schema_max_items,
                    "additionalItems": True,
                }
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_min_max_additional_dict(self):
        """ Normalized System Test

         If ``schema.minItems > schema.maxItems``, not all conditions can be met and therefore raise an exception.

        assert that:
            Even if ``schema.additionalItems`` is dict, when ``schema.items`` is list and both of ``schema.minItems``
            and ``schema.maxItems`` are specified, ``_get_inclusive_integer_range(schema)`` returns
            ``minItems, maxItems``.
        """
        items_list = ([{}],
                      [{"type": "number"}],
                      [{"type": "integer"}, {"type": "number"}],
                      [{"type": "string"}, {"type": "integer"}, {"type": "number"}],
                      [{"type": "null"}, {"type": "string"}, {"type": "integer"}, {"type": "number"}])
        threshold_list = ((0, 0),
                          (0, 1),
                          (1, 1),
                          (1, 2),
                          (1, 3))
        for items, (schema_min_items, schema_max_items) in itertools.product(items_list, threshold_list):
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {
                    "items": items,
                    "minItems": schema_min_items,
                    "maxItems": schema_max_items,
                    "additionalItems": items[0],
                }
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertEqual(max_items, schema_max_items)

    def test_list_length_range_with_tuple_schema_with_min_max_additional_false(self):
        """ Normalized System Test

         If ``schema.minItems > schema.maxItems``, not all conditions can be met and therefore raise an exception.

        assert that:
            When ``schema.additionalItems = False`` and both of ``schema.minItems`` and ``schema.maxItems`` are
            specified and ``schema.minItems <= len(schema.items), ``_get_inclusive_integer_range(schema)`` returns
            ``minItems, min(len(items), maxItems)``.
        """
        parameter_list = ((0, 0, [{"type": "number"}]),
                          (0, 1, [{"type": "number"}]),
                          (1, 1, [{"type": "number"}]),
                          (0, 2, [{"type": "number"}]),
                          (1, 2, [{"type": "number"}]),
                          (0, 1, [{"type": "integer"}, {"type": "number"}]),
                          (1, 1, [{"type": "integer"}, {"type": "number"}]),
                          (0, 2, [{"type": "integer"}, {"type": "number"}]),
                          (1, 2, [{"type": "integer"}, {"type": "number"}]),
                          (2, 2, [{"type": "integer"}, {"type": "number"}]),
                          (0, 3, [{"type": "integer"}, {"type": "number"}]),
                          (1, 3, [{"type": "integer"}, {"type": "number"}]),
                          (2, 3, [{"type": "integer"}, {"type": "number"}]))
        for schema_min_items, schema_max_items, items in parameter_list:
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {
                    "items": items,
                    "minItems": schema_min_items,
                    "maxItems": schema_max_items,
                    "additionalItems": False,
                }
                min_items, max_items = _get_range_of_length(schema, Context.root(schema))
                self.assertEqual(min_items, schema_min_items)
                self.assertEqual(max_items, min(len(items), schema_max_items))

    def test_list_length_range_with_tuple_schema_with_too_large_min_max_additional_false(self):
        """ Semi-normalized System Test

         If ``schema.minItems > schema.maxItems``, not all conditions can be met and therefore raise an exception.

        assert that:
            Even if ``schema.maxItems`` is specified, when ``schema.additionalItems = False`` and
            ``len(schema.items) < schema.minItems``, ``_get_inclusive_integer_range(schema)`` raises
            SchemaConflictError.
        """
        parameter_list = ((2, 2, [{}]),
                          (2, 3, [{"type": "number"}]),
                          (3, 3, [{"type": "number"}]),
                          (3, 4, [{"type": "integer"}, {"type": "number"}]),
                          (4, 4, [{"type": "integer"}, {"type": "number"}]),
                          (5, 10, [{"type": "integer"}, {"type": "number"}]))
        for schema_min_items, schema_max_items, items in parameter_list:
            with self.subTest(items=items, min_items=schema_min_items, max_items=schema_max_items):
                schema = {
                    "items": items,
                    "minItems": schema_min_items,
                    "maxItems": schema_max_items,
                    "additionalItems": False,
                }
                self.assertRaises(SchemaConflictError, lambda: _get_range_of_length(schema, Context.root(schema)))


def _type_to_cls(type_str: str):
    if type_str == "null":
        return None
    elif type_str == "number":
        return float
    elif type_str == "integer":
        return int
    elif type_str == "boolean":
        return bool
    elif type_str == "string":
        return str
    elif type_str == "array":
        return list
    elif type_str == "object":
        return dict
    else:
        raise ValueError(f"Unknown type: {type_str}.")
