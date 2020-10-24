import unittest
from ranj import genlist

class TestGenlist(unittest.TestCase):

    def test_genlist_with_empty_schema(self):
        schema = {}
        self.assertIsInstance(genlist(schema), list)

    def test_genlist_with_tight_length(self):
        schema = {
            "type": "array",
            "minItems": 6,
            "maxItems": 6,
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 6)

    def test_genlist_with_single_items(self):
        schema = {
            "type": "array",
            "minItems": 5,
            "items": {
                "type": "string",
            }
        }
        generated = genlist(schema)
        for item in generated:
            self.assertIsInstance(item, str)

    def test_genlist_with_tuple_items(self):
        schema = {
            "type": "array",
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)

    def test_genlist_with_tuple_items_and_tight_length(self):
        schema = {
            "type": "array",
            "additional_items": True,
            "minItems": 5,
            "maxItems": 5,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 5)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)

    def test_genlist_with_tuple_items_and_tight_length_and_additional_schema(self):
        schema = {
            "type": "array",
            "additional_items": { "type": "bool" },
            "minItems": 5,
            "maxItems": 5,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 5)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)
        self.assertIsInstance(generated[3], bool)
        self.assertIsInstance(generated[4], bool)

    def test_genlist_with_tuple_items_and_same_size_maxItems(self):
        schema = {
            "type": "array",
            "maxItems": 3,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)

    def test_genlist_with_tuple_items_and_same_size_maxItems_and_additional_schema(self):
        schema = {
            "type": "array",
            "maxItems": 3,
            "additional_items": { "type": "bool" },
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)

    def test_genlist_with_tuple_items_and_same_size_maxItems_and_additional_true(self):
        schema = {
            "type": "array",
            "maxItems": 3,
            "additional_items": True,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        generated = genlist(schema)
        self.assertEqual(len(generated), 3)
        self.assertIsInstance(generated[0], str)
        self.assertIsNone(generated[1])
        self.assertIsInstance(generated[2], int)

    def test_genlist_with_tuple_items_and_too_less_maxItems(self):
        schema = {
            "type": "array",
            "maxItems": 2,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        self.assertRaises(Exception, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_less_maxItems_and_additional_schema(self):
        schema = {
            "type": "array",
            "additional_items": { "type": "bool" },
            "maxItems": 2,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        self.assertRaises(Exception, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_less_maxItems_and_additional_true(self):
        schema = {
            "type": "array",
            "additional_items": True,
            "maxItems": 2,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        self.assertRaises(Exception, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_less_maxItems_and_additional_false(self):
        schema = {
            "type": "array",
            "additional_items": False,
            "maxItems": 2,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        self.assertRaises(Exception, lambda: genlist(schema))

    def test_genlist_with_tuple_items_and_too_great_minItems_and_additional_false(self):
        schema = {
            "type": "array",
            "additional_items": False,
            "minItems": 4,
            "items": [
                { "type": "string" },
                { "type": "null" },
                { "type": "integer" },
            ]
        }
        self.assertRaises(Exception, lambda: genlist(schema))
