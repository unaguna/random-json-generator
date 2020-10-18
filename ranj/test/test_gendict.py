import unittest
from ranj import gendict

class TestGennum(unittest.TestCase):

    def test_gennum_with_empty_schema(self):
        schema = {}
        generated = gendict(schema)
        self.assertIsInstance(generated, dict)
        self.assertDictEqual(generated, {})
    
    def test_gennum_with_required(self):
        schema = {
            "required": ["aaa", "bbb"],
        }
        generated = gendict(schema)
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()), set(["aaa", "bbb"]))
    
    def test_gennum_with_required_and_properties(self):
        schema = {
            "required": ["aaa", "bbb"],
            "properties": {
                "aaa": {"type": "number"},
                "bbb": {"type": "object"},
            },
        }
        generated = gendict(schema)
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()), set(["aaa", "bbb"]))
        self.assertIsInstance(generated["aaa"], float)
        self.assertIsInstance(generated["bbb"], dict)
        self.assertDictEqual(generated["bbb"], {})
