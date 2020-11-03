import unittest
from ranjg import genint


class TestGenint(unittest.TestCase):
    """Test class of ``genint``

    Test ``ranjg.genint``
    """

    def test_genint_with_empty_schema(self):
        """ Normalized System Test

        ``genint(schema)`` returns integer value even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``genint(schema)`` returns ``int`` value.
        """
        schema = {}
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertIsInstance(genint(schema), int)

    # TODO: minimum のみを指定するテスト
    # TODO: maximum のみを指定するテスト
    # TODO: exclusiveMinimum (int) のみを指定するテスト
    # TODO: exclusiveMaximum (int) のみを指定するテスト
    # TODO: exclusiveMinimum (bool) のみを指定するテスト
    # TODO: exclusiveMaximum (bool) のみを指定するテスト
    # TODO: minimum, exclusiveMinimum (bool) のみを指定するテスト
    # TODO: maximum, exclusiveMinimum (bool) のみを指定するテスト
    # TODO: maximum, exclusiveMaximum (bool) のみを指定するテスト
    # TODO: minimum, exclusiveMaximum (bool) のみを指定するテスト

    def test_genint_with_tight_min_max(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.maximum`` specified, ``genint(schema)`` returns integer value in range
        [``schema.minimum``, ``schema.maximum``]. So when ``minimum`` value equals ``maximum`` value, the returned value
        equals them.

        assert that:
            When ``schema.minimum`` equals ``schema.maximum``, ``genint(schema)`` returns ``int`` value equal to them.
        """
        # TODO: 複数の値を使って試験する。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "minimum": 5,
            "maximum": 5,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_min_exMax(self):
        """ Normalized System Test

        When ``schema.minimum`` and ``schema.exclusiveMaximum`` specified, ``genint(schema)`` returns integer value in
        range [``schema.minimum``, ``schema.exclusiveMaximum``). So when ``minimum`` value equals
        ``exclusiveMaximum - 1``, the returned value equals ``minimum``.

        assert that:
            When ``schema.minimum`` equals ``schema.exclusiveMaximum - 1``, ``genint(schema)`` returns ``int`` value
            equal to ``minimum``.
        """
        # TODO: 複数の値を使って試験する。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "minimum": 5,
            "exclusiveMaximum": 6,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_exMin_max(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` and ``schema.maximum`` specified, ``genint(schema)`` returns integer value in
        range (``schema.exclusiveMinimum``, ``schema.maximum``]. So when ``maximum`` value equals
        ``exclusiveMinimum + 1``, the returned value equals ``maximum``.

        assert that:
            When ``schema.maximum`` equals ``schema.exclusiveMinimum + 1``, ``genint(schema)`` returns ``int`` value
            equal to ``maximum``.
        """
        # TODO: 複数の値を使って試験する。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "exclusiveMinimum": 4,
            "maximum": 5,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_exMin_exMax(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` and ``schema.exclusiveMaximum`` specified, ``genint(schema)`` returns integer
        value in range (``schema.exclusiveMinimum``, ``schema.exclusiveMaximum``). So when ``exclusiveMinimum`` value
        equals ``exclusiveMaximum - 2``, the returned value is mean of them.

        assert that:
            When ``schema.exclusiveMinimum + 1`` equals ``schema.exclusiveMaximum - 1``, ``genint(schema)`` returns
            ``int`` value equal to them.
        """
        # TODO: 複数の値を使って試験する。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "exclusiveMinimum": 4,
            "exclusiveMaximum": 6,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_min_max_exMinTrue(self):
        """ Normalized System Test

        When ``schema.exclusiveMinimum`` is ``True`` and ``schema.minimum`` specified, ``genint(schema)`` returns
        integer value greater than ``minimum``. So when ``schema.exclusiveMinimum`` is ``True`` and ``maximum`` value
        equals ``minimum + 1``, the returned value equals ``maximum``.

        assert that:
            When``schema.exclusiveMinimum`` is ``True`` and ``schema.maximum`` equals ``schema.minimum + 1``,
            ``genint(schema)`` returns ``int`` value equal to ``maximum``.
        """
        # TODO: 複数の値を使って試験する。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "minimum": 4,
            "exclusiveMinimum": True,
            "maximum": 5,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_min_max_exMaxTrue(self):
        """ Normalized System Test

        ``When ``schema.exclusiveMaximum`` is ``True`` and ``schema.maximum`` specified, ``genint(schema)`` returns
        integer value lower than ``maximum``. So when ``schema.exclusiveMaximum`` is ``True`` and ``minimum`` value
        equals ``maximum - 1``, the returned value equals ``minimum``.

        assert that:
            When``schema.exclusiveMaximum`` is ``True`` and ``schema.minimum`` equals ``schema.maximum - 1``,
            ``genint(schema)`` returns ``int`` value equal to ``minimum``.
        """
        # TODO: 複数の値を使って試験する。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "minimum": 5,
            "maximum": 6,
            "exclusiveMaximum": True,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    # TODO: 矛盾する minimum, maximum を指定するテスト
    # TODO: 矛盾する minimum, exclusiveMaximum (int) を指定するテスト
    # TODO: 矛盾する minimum, maximum, exclusiveMaximum (True) を指定するテスト
    # TODO: 矛盾する minimum, maximum, exclusiveMaximum (False) を指定するテスト
    # TODO: タイトで矛盾しない minimum, maximum, exclusiveMaximum (False) を指定するテスト
    # TODO: 矛盾する exclusiveMinimum (int), maximum を指定するテスト
    # TODO: 矛盾する minimum, exclusiveMinimum (True), maximum を指定するテスト
    # TODO: 矛盾する minimum, exclusiveMinimum (False), maximum を指定するテスト
    # TODO: タイトで矛盾しない minimum, exclusiveMinimum (False), maximum を指定するテスト
    # TODO: minimum, exclusiveMinimum (int) の両方を指定するテスト
    # TODO: maximum, exclusiveMaximum (int) の両方を指定するテスト
