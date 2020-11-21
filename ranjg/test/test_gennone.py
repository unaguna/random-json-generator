import unittest
from ranjg import gennone


class TestGennone(unittest.TestCase):
    """Test class of ``gennone``

    Test ``ranjg.gennone``
    """

    def test_gennone_with_empty_schema(self):
        """ Normalized System Test

        ``gennone()`` returns ``None``. It does nothing else.

        assert that:
            ``gennone()`` returns ``None``.
        """
        self.assertIsNone(gennone())
