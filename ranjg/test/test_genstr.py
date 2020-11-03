import unittest
from ranjg import genstr


class TestGenstr(unittest.TestCase):
    """Test class of ``genstr``

    Test ``ranjg.genstr``
    """

    def test_genstr_with_empty_schema(self):
        """ Normalized System Test

        ``genstr(schema)`` returns a string value. When ``schema`` is empty, the result contains only alphabets.

        assert that:
            When the schema is empty, ``genstr(schema)`` returns ``str`` value contains only alphabets.
        """
        schema = {}
        generated = genstr(schema)
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertIsInstance(generated, str)
        self.assertTrue(generated.isalpha())

    def test_genstr_with_maxLength_0(self):
        """ Normalized System Test

        When ``schema.maxLength`` is specified, ``genstr(schema)`` returns a string value with a length of ``maxLength``
        or less.

        assert that:
            When ``schema.maxLength == 0``, ``genstr(schema)`` returns the empty string.
        """
        schema = {"maxLength": 0}
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertEqual(genstr(schema), "")

    # TODO: schema.maxLength に正の数を指定するテスト
    # TODO: schema.maxLength に負の数を指定するテスト

    def test_genstr_with_minLength(self):
        """ Normalized System Test

        When ``schema.minLength`` is specified, ``genstr(schema)`` returns a string value with a length of ``minLength``
        or more.

        assert that:
            When ``schema.minLength`` is specified, ``genstr(schema)`` returns the string value and it's length is
            greater than or equal to ``minLength``.
        """
        # TODO: 複数の値でテストを行う。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {"minLength": 100}
        generated = genstr(schema)
        self.assertIsInstance(generated, str)
        self.assertGreaterEqual(len(generated), 100)

    # TODO: schema.minLength に負の数を指定するテスト

    def test_genstr_with_length(self):
        """ Normalized System Test

        When ``schema.minLength`` and ``schema.maxLength`` is specified, ``genstr(schema)`` returns a string value with
        a length ``x`` satisfied ``minLength <= x <= maxLength``. As a result, when ``minLength`` and ``maxLength`` have
        same value, the length of the result equals them.

        assert that:
            When ``schema.minLength`` equals to ``schema.maxLength``, ``genstr(schema)`` returns the string with a
            length of them.
        """
        # TODO: 複数の値でテストを行う。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {"minLength": 10, "maxLength": 10}
        generated = genstr(schema)
        self.assertIsInstance(generated, str)
        self.assertEqual(len(generated), 10)

    # TODO: pattern を指定するテスト
