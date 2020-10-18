import unittest
from ranj import genstr

class TestGenstr(unittest.TestCase):

    def test_gennum_with_empty_schema(self):
        schema = {}
        self.assertEqual(genstr(schema), "")
