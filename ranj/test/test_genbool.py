import unittest
from ranj import genbool

class TestGenbool(unittest.TestCase):

    def test_genint_with_empty_schema(self):
        schema = {}
        self.assertIsInstance(genbool(schema), bool)
