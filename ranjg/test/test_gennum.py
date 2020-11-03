import unittest
from ranjg import gennum


class TestGennum(unittest.TestCase):
    """Test class of ``gennum``

    Test ``ranjg.gennum``
    """

    def test_gennum_with_empty_schema(self):
        """ Normalized System Test

        ``gennum(schema)`` returns a number value even if ``schema`` is empty.

        assert that:
            When the schema is empty, ``gennum(schema)`` returns ``float`` value.
        """
        schema = {}
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertIsInstance(gennum(schema), float)

    def test_gennum_with_param_minimum(self):
        """ Normalized System Test

        When ``properties.minimum`` is specified, the result number ``x`` satisfies `` x >= minimum``.

        assert that:
            When the schema has ``minimum``, ``gennum(schema)`` returns ``float`` value ``x`` and it satisfies
            `` x >= minimum``.
        """
        # TODO: 複数の値でテストする。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "minimum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertGreaterEqual(generated, 1.23)

    def test_gennum_with_param_maximum(self):
        """ Normalized System Test

        When ``properties.maximum`` is specified, the result number ``x`` satisfies `` x <= maximum``.

        assert that:
            When the schema has ``maximum``, ``gennum(schema)`` returns ``float`` value ``x`` and it satisfies
            `` x <= maximum``.
        """
        # TODO: 複数の値でテストする。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "maximum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertLessEqual(generated, 1.23)

    def test_gennum_with_param_exclusiveMinimum(self):
        """ Normalized System Test

        When ``properties.exclusiveMinimum`` is specified by a number, the result number ``x`` satisfies
        `` x > exclusiveMinimum``.

        assert that:
            When the schema has ``properties.exclusiveMinimum`` as number, ``gennum(schema)`` returns ``float`` value
            ``x`` and it satisfies `` x > exclusiveMinimum``.
        """
        # TODO: 複数の値でテストする。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "exclusiveMinimum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertGreater(generated, 1.23)

    def test_gennum_with_param_exclusiveMaximum(self):
        """ Normalized System Test

        When ``properties.exclusiveMaximum`` is specified by a number, the result number ``x`` satisfies
        `` x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.exclusiveMaximum`` as number, ``gennum(schema)`` returns ``float`` value
            ``x`` and it satisfies `` x < exclusiveMaximum``.
        """
        # TODO: 複数の値でテストする。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "exclusiveMaximum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertLess(generated, 1.23)

    def test_gennum_with_param_minimum_exclusiveMinimum(self):
        """ Normalized System Test

        When both ``properties.minimum`` and ``properties.exclusiveMinimum: number`` are specified, the result number
        ``x`` satisfies ``x >= maximum`` and ``x > exclusiveMaximum``.

        assert that:
            When the schema has ``properties.minimum`` and ``properties.exclusiveMinimum`` as number, ``gennum(schema)``
            returns ``float`` value ``x`` and it satisfies ``x >= minimum`` and ``x > exclusiveMinimum``.
        """
        # TODO: docstring の assert that 通りの assert を行う
        # TODO: 複数の値でテストする。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "minimum": 1.23E+200,
            "exclusiveMinimum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertGreater(generated, 1.23)

    def test_gennum_with_param_maximum_exclusiveMaximum(self):
        """ Normalized System Test

        When both ``properties.maximum`` and ``properties.exclusiveMaximum: number`` are specified, the result number
        ``x`` satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.

        assert that:
            When the schema has ``properties.maximum`` and ``properties.exclusiveMaximum`` as number, ``gennum(schema)``
            returns ``float`` value ``x`` and it satisfies ``x <= maximum`` and ``x < exclusiveMaximum``.
        """
        # TODO: docstring の assert that 通りの assert を行う
        # TODO: 複数の値でテストする。
        # TODO: 取得した値がスキーマに合致することを確かめる。
        schema = {
            "maximum": 1.23E+200,
            "exclusiveMaximum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertLess(generated, 1.23)
