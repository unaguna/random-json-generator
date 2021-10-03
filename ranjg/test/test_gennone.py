import unittest

from ..factories import NoneFactory


class TestNoneFactory(unittest.TestCase):
    """Test class of ``NoneFactory``

    Test ``NoneFactory``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``NoneFactory(schema).gen()`` returns ``None``. It does nothing else.

        assert that:
            ``NoneFactory(schema).gen()`` returns ``None``.
        """
        self.assertIsNone(NoneFactory({}).gen())
