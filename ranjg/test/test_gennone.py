import unittest
from ranjg import gennone


class TestGennone(unittest.TestCase):

    def test_gennone_with_empty_schema(self):
        self.assertIsNone(gennone())
