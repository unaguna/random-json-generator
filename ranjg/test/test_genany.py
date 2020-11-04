import unittest
from ranjg import genany


class TestGenany(unittest.TestCase):
    """Test class of ``genany``

    Test ``ranjg.genany``
    """

    def test_genany_with_empty_schema(self):
        """ Normalized System Test

        ``genany(schema)`` returns something.

        assert that:
            ``genany(schema)`` returns without raising any exceptions.
        """
        schema = {}
        genany(schema)
