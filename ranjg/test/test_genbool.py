import unittest
from ranjg import genbool


class TestGenbool(unittest.TestCase):

    def test_genbool_with_empty_schema(self):
        self.assertIsInstance(genbool(), bool)
