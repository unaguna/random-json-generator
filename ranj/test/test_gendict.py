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
            "required": ["aaa", "bbb", "ccc", "ddd", "eee", "xxx", "zzz"],
            "properties": {
                "aaa": {"type": "number"},
                "bbb": {"type": "object"},
                "ccc": {"type": "string"},
                "ddd": {"type": "boolean"},
                "eee": {"type": "array"},
                "xxx": {"type": "null"},
                "zzz": {},
            },
        }
        generated = gendict(schema)
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()), set(["aaa", "bbb", "ccc", "ddd", "eee", "xxx", "zzz"]))
        self.assertIsInstance(generated["aaa"], float)
        self.assertIsInstance(generated["bbb"], dict)
        self.assertDictEqual(generated["bbb"], {})
        self.assertIsInstance(generated["ccc"], str)
        self.assertIsInstance(generated["ddd"], bool)
        self.assertIsInstance(generated["eee"], list)
        self.assertIsNone(generated["xxx"])
