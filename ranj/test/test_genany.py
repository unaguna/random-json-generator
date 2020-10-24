import unittest
from ranj import genany

class TestGenany(unittest.TestCase):

    def test_genany_with_empty_schema(self):
        schema = {}
        genany(schema)
