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
    
