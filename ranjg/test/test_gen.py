import unittest
from ranjg import gen

class TestGen(unittest.TestCase):

    def test_gen_with_empty_schema(self):
        schema = {}
        gen(schema)

    def test_gen_with_schema_file_path(self):
        gen(schema_file="./test-resources/schema-legal-type_str.json")



