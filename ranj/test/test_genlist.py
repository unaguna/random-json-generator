import unittest
from ranj import genlist

class TestGenlist(unittest.TestCase):

    def test_genlist_with_empty_schema(self):
        schema = {}
        self.assertIsInstance(genlist(schema), list)
