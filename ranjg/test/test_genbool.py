import unittest
from ranjg import genbool


class TestGenbool(unittest.TestCase):
    """Test class of ``genbool``

    Test ``ranjg.genbool``
    """

    def test_genbool(self):
        """ Normalized System Test

        ``genbool()`` returns ``True`` or ``False`` randomly.

        assert that:
            ``genbool()`` returns boolean value.
        """
        self.assertIsInstance(genbool(), bool)
